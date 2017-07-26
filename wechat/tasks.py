from datetime import timedelta
from celery.task import periodic_task
from celery.task.control import revoke

from wechat.celery import app
from wxpy.exceptions import ResponseError
from itchat.signals import logged_out


def restart_listener(sender, **kw):
    task_id = r.get(LISTENER_TASK_KEY)
    if task_id:
        revoke(str(task_id, 'utf-8'))
    task_id = app.send_task('wechat.tasks.listener')
    r.set(LISTENER_TASK_KEY, task_id)


logged_out.connect(restart_listener)

from wxpy.signals import stopped
from libs.wx import gen_avatar_path, get_bot
from views.api import json_api
from models.redis import db as r, LISTENER_TASK_KEY
from app import app as sse_api
from ext import db, sse
from models.core import User, Group, MP  # noqa
from models.messaging import Notification

stopped.connect(restart_listener)
MP_FIELD = ['nick_name', 'signature', 'province', 'city']
USER_FIELD = MP_FIELD + ['sex']
bot = get_bot()


def _retrieve_data(update=False):
    _update_contact(bot, update)
    _update_group(bot, update)
    _update_mp(bot, update)


def _get_self(bot):
    myself = db.session.query(User).get(bot.self.puid)
    if myself is None:
        myself = User.create(id=bot.self.puid, **{
            field: getattr(bot.self, field) for field in USER_FIELD})
    return myself


def _update_group(bot, update=False):
    session = db.session
    wx_groups = bot.groups(update)
    myself = _get_self(bot)
    wx_ids = set([g.puid for g in wx_groups])
    groups = session.query(Group).filter(Group.owner_id == bot.self.puid).all()
    local_ids = set([g.id for g in groups])

    need_del = local_ids.difference(wx_ids)
    for group in groups:
        if group.id in need_del:
            myself.groups.remove(group)
            db.session.delete(group)

    for g in wx_groups:
        group = session.query(Group).get(g.puid)
        if not group:
            group = Group.create(id=g.puid, nick_name=g.nick_name,
                                 owner_id=bot.self.puid)
        local_ids = set([u.id for u in group.members])
        wx_ids = set([u.puid for u in g.members])
        need_add = wx_ids.difference(local_ids)
        if need_add:
            for u in g.members:
                if u.puid in need_add:
                    user = User.create(id=u.puid, **{field: getattr(u, field)
                                                     for field in USER_FIELD})
                    group.add_member(user)
                _, path, need_update = gen_avatar_path(u.puid)
                if need_update:
                    try:
                        u.get_avatar(path)
                    except (ResponseError, KeyError):
                        print('No member: {}'.format(u.puid))
        need_del = local_ids.difference(wx_ids)
        if need_del:
            for u in group.members:
                if u.id in need_del:
                    group.del_member(u)
        _, path, need_update = gen_avatar_path(g.puid)
        if need_update:
            g.get_avatar(path)
    session.commit()


def _update_mp(bot, update=False):
    session = db.session
    myself = _get_self(bot)
    wx_mps = bot.mps(update)
    local_ids = set([m.id for m in myself.mps])
    wx_ids = set([u.puid for u in wx_mps])
    need_add = wx_ids.difference(local_ids)
    if need_add:
        for m in wx_mps:
            # see https://github.com/dongweiming/wechat-admin/issues/14
            if m.puid is None:
                continue
            if m.puid in need_add:
                mp = MP.create(id=m.puid, **{field: getattr(m, field)
                                             for field in MP_FIELD})
                # wxpy还不支持公众号的头像下载
                myself.mps.append(mp)
    need_del = local_ids.difference(wx_ids)
    if need_del:
        for mp in myself.mps:
            if mp.id in need_del:
                myself.mps.remove(mp)
                db.session.delete(mp)
    session.commit()


def _update_contact(bot, update=False):
    session = db.session
    myself = _get_self(bot)
    wx_friends = bot.friends(update)
    local_ids = set([u.id for u in myself.friends.all()])
    wx_ids = set([u.puid for u in wx_friends])
    need_add = wx_ids.difference(local_ids)
    if need_add:
        for u in wx_friends:
            if u.puid in need_add:
                user = User.create(id=u.puid, **{field: getattr(u, field)
                                                 for field in USER_FIELD})
                myself.add_friend(user)
            _, path, need_update = gen_avatar_path(u.puid)
            if need_update:
                try:
                    u.get_avatar(path)
                except ResponseError:
                    print('No member: {}'.format(u.puid))
    need_del = local_ids.difference(wx_ids)
    if need_del:
        for u in myself.friends:
            if u.id in need_del:
                myself.del_friend(u)
    session.commit()


@app.task
def listener():
    from libs.listener import bot
    with json_api.app_context():
        bot.join()


@app.task
def retrieve_data():
    with json_api.app_context():
        _retrieve_data()


@app.task
def update_contact(update=False):
    with json_api.app_context():
        _update_contact(bot, update=update)


@app.task
def update_group(update=False):
    with json_api.app_context():
        _update_group(bot, update=update)


@periodic_task(run_every=timedelta(seconds=60), time_limit=5)
def send_notify():
    count = Notification.count_by_receiver_id(bot.self.puid)
    with sse_api.app_context():
        sse.publish({'count': count}, type='notification')

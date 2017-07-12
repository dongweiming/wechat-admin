# TODO:
# 1. puid过期后顺便也删掉对应的头像

import os
from datetime import datetime, timedelta

from itchat.signals import scan_qr_code, confirm_login, logged_in, logged_out
from wxpy.exceptions import ResponseError

from ext import db, sse
from config import avatar_tmpl

here = os.path.abspath(os.path.dirname(__file__))
MP_FIELD = ['sex', 'nick_name', 'signature', 'province', 'city']
USER_FIELD = MP_FIELD + ['sex']


def publish(uuid, **kw):
     from app import app
     with app.app_context():
         params = {'uuid': uuid, 'extra': kw.pop('extra', None),
                   'type': kw.pop('type', None)}
         params.update(kw)
         sse.publish(params, type='login')


scan_qr_code.connect(publish)
confirm_login.connect(publish)
logged_out.connect(publish)

from wxpy import * # noqa


def get_bot():
    bot = Bot('bot.pkl', qr_path=os.path.join(
        here, '../static/img/qr_code.png'))
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot


from models.core import User, Group, MP  # noqa


def gen_avatar_path(puid, force=False):
    need_update = True
    avatar_url = avatar_tmpl.format(puid)
    avatar_path = os.path.join(here, '../{}'.format(avatar_url))
    if os.path.exists(avatar_path):
        mtime = datetime.fromtimestamp(os.stat(avatar_path).st_mtime)
        if datetime.now() - mtime < timedelta(days=1) and not force:
            need_update = False
    return avatar_url, avatar_path, need_update


def get_logged_in_user(bot):
    user_ = bot.self
    id = user_.puid
    url, path, need_update = gen_avatar_path(id, force=True)
    bot.core.get_head_img(picDir=path)
    user = {
        'id': id,
        'avatar': url,
        'name': user_.nick_name
    }
    return user


def retrieve_data(update=False):
    bot = get_bot()
    session = db.session
    # update group
    for g in bot.groups(update):
        group = session.query(Group).get(g.puid)
        if not group:
            group = Group.create(id=g.puid, nick_name=g.nick_name)
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
    # update mp
    myself = session.query(User).get(bot.self.puid)
    wx_mps = bot.mps()
    local_ids = set([m.id for m in myself.mps])
    wx_ids = set([u.puid for u in wx_mps])
    need_add = wx_ids.difference(local_ids)
    if need_add:
        for m in wx_mps:
            if m.puid in need_add:
                User.create(id=m.puid, **{field: getattr(m, field)
                                          for field in MP_FIELD})
                # wxpy还不支持公众号的头像下载
    need_del = local_ids.difference(wx_ids)
    if need_del:
        for mp in myself.mps:
            if mp.id in need_del:
                db.session.delete(mp)
    # update contact
    myself = session.query(User).get(bot.self.puid)
    wx_friends = bot.friends()
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

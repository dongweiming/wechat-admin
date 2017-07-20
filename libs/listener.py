# coding=utf-8
import os
import re
import sys

from wxpy import Friend, Group, Chat, MP as _MP
from wxpy.api import consts

from config import PLUGIN_PATHS, PLUGINS
from libs.consts import *
from libs.globals import current_bot as bot
from models.admin import GroupSettings
from models.messaging import Message, Notification, db

uid = bot.self.puid
settings = GroupSettings.get(uid)
pattern_map = {p: tmpl for p, tmpl in settings.group_patterns}
new_member_regex = re.compile(r'^"(.+)"通过|邀请"(.+)"加入|')
all_types = [k.capitalize() for k in dir(consts) if k.isupper() and k != 'SYSTEM']
here = os.path.abspath(os.path.dirname(__file__))
UPLOAD_PATH = os.path.join(here, '../static/img/uploads')
if not os.path.exists(UPLOAD_PATH):
    os.mkdir(UPLOAD_PATH)

groups = [g for g in bot.groups() if g.owner.puid == uid]


def get_creators():
    creator_ids = settings.creators
    try:
        creators = map(lambda x: bot.friends().search(puid=x)[0],
                       creator_ids)
    except IndexError:
        users = [u.to_dict() for u in db.session.query(User).filter(
            User.id.in_(creator_ids)).all()]
        creators = map(lambda x: bot.friends().search(
            u['nick_name'], Sex=u['sex'], Signature=u['signature'])[0], users)
    return list(creators)


def invite(user, pattern):
    groups = sorted(bot.groups(update=True).search(pattern),
                    key=lambda x: x.name)
    if len(groups) > 0:
        for group in groups:
            if len(group.members) == 500:
                continue
            if user in group:
                content = "您已经加入了{} [微笑]".format(group.nick_name)
                user.send(content)
            else:
                group.add_members(user, use_invitation=True)
            return
        else:
            next_topic = pattern_map[pattern].format(
                re.search(r'\d+', s).group() + 1)
            new_group = bot.create_group(get_creators(), topic=next_topic)
    else:
        print('Invite Failed')


@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    pattern = next((p for p in pattern_map if p in msg.text.lower()), None)
    if pattern is not None:
        invite(user, pattern)
    else:
        user.send(settings.invite_text)


@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    pattern = next((p for p in pattern_map if p in msg.text.lower()), None)
    if pattern is not None:
        invite(msg.sender, pattern)


@bot.register(groups, NOTE)
def welcome(msg):
    match = new_member_regex.search(msg.text)
    if match:
        text = list(filter(lambda x:x, match.groups()))
        if text:
            return settings.welcome_text.format(text[0])


@bot.register(msg_types=all_types, except_self=False)
def send_msg(m):
    # wxpy还不支持未命名的群聊消息
    # 先忽略腾讯新闻之类发的信息
    if m.receiver.name is None or m.sender is None:
        return
    msg_type = TYPE_TO_ID_MAP.get(m.type, 0)
    if isinstance(m.sender, Group):
        sender_id = m.member.puid
        group_id = m.chat.puid
    elif isinstance(m.sender, _MP):
        sender_id = m.sender.puid
        group_id = 0
        msg_type = TYPE_TO_ID_MAP.get('MP')
    else:
        sender_id = m.sender.puid
        group_id = 0
    receiver_id = m.receiver.puid
    from views.api import json_api as app
    with app.app_context():
        msg = Message.create(sender_id=sender_id, receiver_id=receiver_id,
                             content=m.text, url=m.url, type=msg_type,
                             receive_time=m.receive_time, group_id=group_id)
        if m.type in (PICTURE, RECORDING, ATTACHMENT, VIDEO):
            _, ext = os.path.splitext(m.file_name)
            m.get_file(os.path.join(UPLOAD_PATH, '{}{}'.format(msg.id, ext)))
            msg.file_ext = ext
            db.session.commit()
        Notification.add(receiver_id, msg.id)


_sys_path = sys.path[:]
for pluginpath in PLUGIN_PATHS:
    sys.path.insert(0, pluginpath)

_cached = {}
_namespace = {}
_patterns = []
for p in PLUGINS:
    if isinstance(p, str):
        try:
            mod = __import__(p, globals(), locals(), 'module')
        except ImportError as e:
            print('Cannot load plugin `{}`\n{}'.format(p, e))
            continue
        plugin = mod.export()
    else:
        plugin = p
    try:
        name = getattr(plugin, 'name')
    except AttributeError:
        print("Plugin `{}` has no attribute 'name'".format(p))
        continue
    _cached[name] = plugin
    def func(msg, name=name, plugin=plugin):
        patterns = getattr(plugin, 'patterns', None) or []
        text = msg.text.lower()
        if patterns:
            if getattr(plugin, 'exclusive', False):
                _patterns.extend(patterns)
            if not re.search(r'{}'.format(patterns), text):
                return
        ex_patterns = getattr(plugin, 'exclude_patterns', None) or []
        ex_patterns = set(_patterns + ex_patterns +
                          pattern_map.keys()).difference(patterns)
        patterns = '|'.join(ex_patterns)
        if re.search(r'{}'.format(patterns), text):
            return
        from views.api import json_api as app
        with app.app_context():
            app.plugin_modules = _cached
            msg.sender.send(plugin.main(msg))

    exec('def {}(msg):\n    return func(msg)'.format(name),
         {'func': func}, _namespace)
    bot.register(msg_types=getattr(plugin, 'msg_types', None),
                 run_async=getattr(plugin, 'run_async', True),
                 chats=getattr(plugin, 'chats', None),
                 except_self=getattr(plugin, 'except_self', None)
    )(_namespace[name])

sys.path = _sys_path

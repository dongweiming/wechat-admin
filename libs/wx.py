# TODO:
# 1. puid过期后顺便也删掉对应的头像

import os
from datetime import datetime, timedelta

from itchat.signals import scan_qr_code, confirm_login, logged_out

from ext import sse
from config import avatar_tmpl

here = os.path.abspath(os.path.dirname(__file__))


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

from wxpy import *  # noqa


def get_bot():
    bot = Bot('bot.pkl', qr_path=os.path.join(
        here, '../static/img/qr_code.png'), console_qr=None)
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot


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
    try:
        bot.core.get_head_img(picDir=path)
    except FileNotFoundError:
        os.mkdir(os.path.dirname(path))
        bot.core.get_head_img(picDir=path)
    user = {
        'id': id,
        'avatar': url,
        'name': user_.nick_name
    }
    return user

import os

HERE = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/test?charset=utf8mb4'  # noqa
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = 'redis://localhost:6379'
SESSION_TYPE = 'redis'
avatar_tmpl = '/static/img/avatars/{}.jpg'
UPLOAD_FOLDER = os.path.join(HERE, 'uploads')
PIC_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

GROUP_MEMBERS_LIMIT = 500

welcome_text = '🎉 欢迎 @{} 的加入！'
invite_text = '''欢迎您！
请输入关键字 Python 加入群。

本群聊为技术讨论群，入群须知：

1、禁止频繁灌水
2、禁止发广告或者无关技术的链接
3、禁止骚扰和人身攻击
4、请对不甚了解的领域保持敬畏，以免看起来像个小丑
5、不要把负面的情绪带进来
6、禁止私自把群成员拉新群推销

请言行遵守群内规定，违规者将被永远T出。

群成员可发起移出成员投票，语句是 `移出|移除|踢出|T @XXX`

更多功能请向群主发送 help 获得更多功能'''
kick_text = '''
正在投票移出 @{member}

当前 {current} / {total} 票 ({period} 秒有效)

移出成员会造成其不能再进去本群，请勿滥用投票功能！🤔🤔🤔
'''

group_patterns = [
    ['python', 'Python✌{}群'],
    ['web', 'Web技术交流{}群'],
]

PLUGIN_PATHS = [os.path.join(HERE, 'wechat-plugins')]
PLUGINS = ['chatter', 'help', 'tuling']  # simsimi和chatter只能2选一

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

try:
    from local_settings import *  # noqa
except ImportError:
    pass

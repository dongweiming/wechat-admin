import os

HERE = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/test?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = 'redis://localhost:6379'
SESSION_TYPE = 'redis'
avatar_tmpl = '/static/img/avatars/{}.jpg'
UPLOAD_FOLDER = os.path.join(HERE, 'uploads')
PIC_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

group_tmpl = 'Python✌{}群'
welcome_text = '🎉 欢迎 @{} 的加入！'
invite_text = '''欢迎您！
请输入关键字 Python 加入群：

进群四件事：

1、阅读群公告，
2、修改群名片，
3、做自我介绍，
4、要是发红包，总额请不要低于50

请言行遵守群内规定，违规者将受到处罚，拉入黑名单。'''

PLUGIN_PATHS = [os.path.join(HERE, 'wechat-plugins')]
PLUGINS = ['simsim']

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

try:
    from local_settings import *  # noqa
except ImportError:
    pass

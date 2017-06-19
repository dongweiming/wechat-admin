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

try:
    from local_settings import *  # noqa
except ImportError:
    pass

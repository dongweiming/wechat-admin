from redis import Redis
from rq import Queue

from libs.wx import retrieve_data as _retrieve_data
from config import REDIS_URL

q = Queue(connection=Redis.from_url(REDIS_URL))


def retrieve_data():
    from views.api import json_api as app
    with app.app_context():
        _retrieve_data()


def async_retrieve_data(bot):
    return q.enqueue(retrieve_data, timeout=1200)

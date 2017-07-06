from datetime import timedelta
from celery.task import periodic_task
from celery.task.control import revoke

from wechat.celery import app

from libs.wx import retrieve_data as _retrieve_data
from wxpy.signals import stopped
from views.api import json_api
from models.base import r, LISTENER_TASK_KEY
from app import app as sse_api
from ext import db, sse
from models.messaging import Message, Notification


def restart_listener():
    task_id = r.get(LISTENER_TASK_KEY)
    if task_id:
        revoke(task_id)
    task_id = app.send_task('wechat.tasks.listener')
    r.set(LISTENER_TASK_KEY, task_id)


stopped.connect(restart_listener)

from libs.listener import bot


@app.task
def listener():
    with json_api.app_context():
        bot.join()


@app.task
def async_retrieve_data():
    with json_api.app_context():
        _retrieve_data()


@periodic_task(run_every=timedelta(seconds=60), time_limit=5)
def send_notify():
    count = Notification.count_by_receiver_id(bot.self.puid)
    with sse_api.app_context():
        sse.publish({'count': count}, type='notification')

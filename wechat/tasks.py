from datetime import timedelta
from celery.task import periodic_task

from wechat.celery import app

from libs.wx import retrieve_data as _retrieve_data
from libs.listener import bot
from views.api import json_api
from app import app as sse_api
from ext import db, sse
from models.messaging import Message, Notification


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

from wechat.celery import app

from libs.wx import retrieve_data as _retrieve_data
from libs.listener import bot
from views.api import json_api


@app.task
def listener():
    with json_api.app_context():
        bot.join()


@app.task
def async_retrieve_data():
    with json_api.app_context():
        _retrieve_data()

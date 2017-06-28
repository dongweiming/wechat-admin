from celery import Celery

app = Celery('wechat', include=['wechat.tasks'])
app.config_from_object('wechat.celeryconfig')


if __name__ == '__main__':
    app.start()

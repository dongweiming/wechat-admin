from celery import Celery
from celery.signals import worker_ready
from celery.schedules import crontab

app = Celery('wechat', include=['wechat.tasks'])
app.config_from_object('wechat.celeryconfig')


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        sender.app.send_task('wechat.tasks.listener')


if __name__ == '__main__':
    app.start()

from celery import Celery
from celery.signals import worker_ready
from celery.schedules import crontab

from models.base import r, LISTENER_TASK_KEY

app = Celery('wechat', include=['wechat.tasks'])
app.config_from_object('wechat.celeryconfig')


@worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        task_id = sender.app.send_task('wechat.tasks.listener')
        r.set(LISTENER_TASK_KEY, task_id)

if __name__ == '__main__':
    app.start()

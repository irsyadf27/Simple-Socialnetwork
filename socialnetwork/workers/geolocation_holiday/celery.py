import os

from celery import Celery

from tasks.geolocation_holiday import geolocation_holiday

app = Celery(
    "geolocation_holiday",
    backend="rpc://",
    broker="amqp://guest:guest@127.0.0.1:5672",
)

app.autodiscover_tasks()

app.conf.update(
    task_compression="bzip2",
    timezone="Asia/Jakarta",
)

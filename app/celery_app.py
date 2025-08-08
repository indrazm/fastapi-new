from celery import Celery

app = Celery('tasks', broker='redis://localhost:6377/0')

app.autodiscover_tasks(['app.tasks'])

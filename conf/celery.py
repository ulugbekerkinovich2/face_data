import os
from celery import Celery
from celery.schedules import crontab

# Django settings modulini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

# Celery ilovasini yaratish
app = Celery('conf')

# Django sozlamalarini Celery'ga yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django ilovalardan avtomatik vazifalarni yuklash
app.autodiscover_tasks()

# Celery Beat jadval sozlamalari
app.conf.beat_schedule = {
    'face-id': {
        'task': 'basic_app.tasks.backup_database',  # To'g'ri vazifa yo'li
        'schedule': crontab(minute='*/30'),
    },
    'get-list-management': {
        'task': 'basic_app.tasks.get_list_management_task',
        'schedule': crontab(minute='*/20'),
    }
}

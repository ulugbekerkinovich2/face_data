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
# print('ok')
# Celery Beat jadval sozlamalari
app.conf.beat_schedule = {
    # 'face-id': {
    #     'task': 'basic_app.tasks.backup_database',  # To'g'ri vazifa yo'li
    #     'schedule': crontab(minute='*/30'),
    # },
    # 'get-list-management': {
    #     'task': 'basic_app.tasks.get_list_management_task',
    #     'schedule': crontab(minute='*/10'),
    # },
    'get-control-logs': {
        'task': 'basic_app.tasks.fetch_and_store_control_logs',
        'schedule': crontab(minute='*/1'),
    },
    # 'upload-and-delete-media-every-10-minutes': {
    #     'task': 'basic_app.tasks.upload_then_delete_media_via_sftp',  # Rsync versiyasi
    #     'schedule': crontab(minute='*/2'),  # Har 10 daqiqada ishlaydi
    # },
}

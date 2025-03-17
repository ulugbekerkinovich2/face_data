import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Sync local media/ folder to remote Django server'

    def handle(self, *args, **kwargs):
        local_media_path = '/absolute/path/to/your/local/media/'  # <-- E'tibor bering
        remote_user = 'root'
        remote_host = '185.217.131.98'
        remote_path = '/var/www/workers/face_data_admin/media/'

        rsync_command = [
            'rsync', '-avz', '--delete',
            local_media_path,
            f'{remote_user}@{remote_host}:{remote_path}'
        ]

        self.stdout.write("🔄 Syncing media folder to server...")

        try:
            subprocess.run(rsync_command, check=True)
            self.stdout.write(self.style.SUCCESS("✅ Media synced successfully!"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"❌ Sync failed: {e}"))

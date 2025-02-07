import os
import requests
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

# Telegram bot sozlamalari
TOKEN = "7850408357:AAFZ8s4Hqjso5XclrAh6xkblW5sOO9O-X9w"  # O'zingizning tokeningiz
CHAT_ID = -1002355350437  # O'zingizning chat ID

class Command(BaseCommand):
    help = "Backup the database and send it to Telegram"

    def handle(self, *args, **kwargs):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default'].get('HOST', 'localhost')
        db_port = settings.DATABASES['default'].get('PORT', '5432')
        backup_file = f"{db_name}_backup.sql"

        try:
            # Use the correct PostgreSQL user
            command = f"PGPASSWORD='{db_password}' pg_dump -h {db_host} -p {db_port} -U {db_user} {db_name} > {backup_file}"
            subprocess.run(command, shell=True, check=True)
            self.stdout.write(self.style.SUCCESS(f"Backup successful: {backup_file}"))

            # Send to Telegram
            self.send_to_telegram(backup_file)

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Backup failed: {e}"))

    def send_to_telegram(self, file_path):
        url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        with open(file_path, "rb") as file:
            files = {"document": file}
            data = {"chat_id": CHAT_ID, "caption": "Database Backup"}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("Backup sent to Telegram successfully."))
            else:
                self.stderr.write(self.style.ERROR(f"Failed to send backup: {response.text}"))
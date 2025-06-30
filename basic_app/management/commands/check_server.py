import time
import requests
from django.core.management.base import BaseCommand

# ✅ Telegram sozlamalari
BOT_TOKEN = '7834818902:AAEWBHQo_Pn3PteZwA4gP6vTiebh99f4-hA'
CHAT_ID = '935920479'

def send_telegram_message(message: str):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data, timeout=5)
        print("Telegram javobi:", response.status_code, response.text)
    except Exception as e:
        print("Telegramga yuborilmadi:", e)

class Command(BaseCommand):
    help = 'Checks if the Django server is running every 11 seconds.'

    def handle(self, *args, **kwargs):
        server_url = 'http://127.0.0.1:8000'

        self.stdout.write(self.style.SUCCESS('📡 Server monitoring boshlandi...'))
        send_telegram_message("📡 Server monitoring boshlandi.")

        last_status = None

        while True:
            try:
                response = requests.get(server_url, timeout=5)
                print("Server javobi:", response.status_code)

                if response.status_code == 404:
                    msg = "✅ Django server ISHLAYAPTI (status 404)!"
                    send_telegram_message(msg)
                    self.stdout.write(self.style.SUCCESS(msg))
                    last_status = "up"
                else:
                    msg = f"⚠️ Server javob berdi, lekin status: {response.status_code}"
                    send_telegram_message(msg)
                    self.stdout.write(self.style.WARNING(msg))
                    last_status = "warn"

            except requests.exceptions.ConnectionError:
                if last_status != "down":
                    msg = "❌ Django server ISHDAN CHIQDI!"
                    send_telegram_message(msg)
                    self.stdout.write(self.style.ERROR(msg))
                    last_status = "down"

            time.sleep(60)

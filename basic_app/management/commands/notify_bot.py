import requests
from django.conf import settings

BOT_TOKEN = settings.BOT_TOKEN
MENTALABA_ARRIVAL_GROUP_CHAT_ID = settings.MENTALABA_ARRIVAL_GROUP_CHAT_ID

def mt_send_group_message(text: str):
    """
    Telegram API orqali to'g'ridan-to'g'ri groupga habar yuboradi.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MENTALABA_ARRIVAL_GROUP_CHAT_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    return response.json()

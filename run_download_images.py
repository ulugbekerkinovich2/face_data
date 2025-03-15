import os
import django
import time
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
django.setup()

if __name__ == "__main__":
    while True:
        print("⏳ Checking missing images...")
        call_command("download_missing_images")
        print("✅ Done. Sleeping 10 minutes.")
        time.sleep(180)  # 10 daqiqa

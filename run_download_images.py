import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")  # <-- loyihangiz nomi

django.setup()

if __name__ == "__main__":
    print("⏳ Starting image sync...")
    call_command("download_missing_images")
    print("✅ Done.")

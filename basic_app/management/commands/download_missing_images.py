import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from basic_app.models import ControlLog, UsersManagement, StrangerCapture


def ensure_image_downloaded(field_file, base_url=None):
    if not field_file or not field_file.name:
        return

    file_path = field_file.path
    file_name = field_file.name

    if os.path.exists(file_path):
        return

    if base_url:
        url = f"{base_url.rstrip('/')}/{file_name}"
    else:
        url = f"http://face-admin.misterdev.uz/media/{file_name}"

    try:
        print(f"📥 Downloading: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Saved: {file_path}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")


class Command(BaseCommand):
    help = 'Download missing images from media server for all models'

    def handle(self, *args, **options):
        base_url = "http://face-admin.misterdev.uz/media"

        models_to_process = [
            (ControlLog, 'image'),
            (UsersManagement, 'image'),
            (StrangerCapture, 'image_file'),
        ]

        for model, field_name in models_to_process:
            self.stdout.write(f"📂 Processing {model.__name__}...")
            queryset = model.objects.exclude(**{field_name: None})
            for obj in queryset:
                image_field = getattr(obj, field_name, None)
                ensure_image_downloaded(image_field, base_url=base_url)
            self.stdout.write(self.style.SUCCESS(f"✅ Done with {model.__name__}"))

        self.stdout.write(self.style.SUCCESS("🎉 All images processed."))

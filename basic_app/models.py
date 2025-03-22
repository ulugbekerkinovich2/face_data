from django.db import models
from datetime import datetime
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from basic_app.services.add_user import add_user
from basic_app.services.gen_random import generate_random_number
from basic_app.services.upload_image import send_image_to_management, send_image_to_controllog

class Heartbeat(models.Model):
    device_id = models.IntegerField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=50, blank=True, null=True)
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Heartbeat from Device {self.device_id} at {self.time}"
    class Meta:
        verbose_name_plural = "Heartbeats"
        # ordering = ['-time']
        verbose_name = "Heartbeat"
        indexes = [
            models.Index(fields=['device_id', 'time']),  # Adding index on device_id and time
        ]


class VerifyPush(models.Model):
    person_id = models.IntegerField()
    device_id = models.IntegerField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    similarity1 = models.FloatField()
    similarity2 = models.FloatField()
    verify_status = models.IntegerField()
    verify_type = models.IntegerField()
    person_type = models.IntegerField()
    name = models.CharField(max_length=255)
    gender = models.IntegerField()
    nation = models.IntegerField()
    card_type = models.IntegerField()
    id_card = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    telnum = models.CharField(max_length=20, blank=True, null=True)
    native = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    mj_card_from = models.IntegerField()
    mj_card_no = models.CharField(max_length=255)
    rfid_card = models.CharField(max_length=255)
    tempvalid = models.IntegerField()
    customize_id = models.IntegerField()
    person_uuid = models.CharField(max_length=255, blank=True, null=True)
    valid_begin = models.DateTimeField(blank=True, null=True)
    valid_end = models.DateTimeField(blank=True, null=True)
    send_in_time = models.IntegerField()
    direction = models.IntegerField()
    sz_qr_code_data = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "verify_push"
        verbose_name = "Verify Push"
        verbose_name_plural = "Verify Pushes"
        indexes = [
            models.Index(fields=['person_id', 'verify_status']),
            models.Index(fields=['create_time']),
            models.Index(fields=['id_card']),  # Example of indexing the ID card field
        ]

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"


class ICCardInfoPush(models.Model):
    device_id = models.IntegerField()
    ic_card_num = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True, default='aniqlanmagan')

    def __str__(self):
        return f"ICCardInfoPush from Device {self.device_id}"
    
    class Meta:
        verbose_name_plural = "ICCard Info Pushes"
        verbose_name = "ICCard Info Push"
        indexes = [
            models.Index(fields=['device_id', 'created_at']),  # Index for device_id and created_at
        ]


class StrangerCapture(models.Model):
    image_file = models.ImageField(upload_to="stranger_captures/", blank=True, null=True)
    create_time = models.DateTimeField()
    device_id = models.IntegerField()
    direction = models.IntegerField()
    picture_type = models.IntegerField()
    send_in_time = models.IntegerField()
    operator = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=255, blank=True, null=True, default='aniqlanmagan')
    
    def __str__(self):
        return f"StrangerCapture from Device {self.device_id} at {self.create_time}"
    class Meta:
        verbose_name_plural = "Stranger Captures"
        verbose_name = "Stranger Capture"
        indexes = [
            models.Index(fields=['device_id', 'create_time']),
            models.Index(fields=['direction']),  # Index for direction field
        ]


class UsersManagement(models.Model):
    face_id = models.IntegerField(null=True, blank=True)
    uid = models.BigIntegerField()
    name = models.TextField(null=True, blank=True)
    type = models.BigIntegerField(null=True, blank=True)
    rf_id_card_num = models.BigIntegerField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    dwfiletype = models.BigIntegerField(null=True, blank=True)
    dwfileindex = models.BigIntegerField(null=True, blank=True)
    dwfilepos = models.BigIntegerField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    RanId = models.BigIntegerField(null=True, blank=True)
    image  = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if isinstance(self.time, str) and "/" in self.time:
            self.time = datetime.strptime(self.time, "%Y-%m-%d/%H:%M:%S")
        super(UsersManagement, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Users Management"
        verbose_name = "User Management"


@receiver(post_save, sender=UsersManagement)
def update_user_image(sender, instance, created, **kwargs):
    """
    When a user is created or updated, send their image to all Face ID devices if available.
    """
    action = "Created" if created else "Updated"
    logging.info(f"🚀 User {action}: {instance.name} (UID: {instance.uid}) - Syncing image to Face ID devices")

    if instance.image:
        try:
            image_path = instance.image.path
            send_image_to_management(instance.id, image_path)
        except Exception as e:
            logging.error(f"❌ Error sending image: {e}")


class StrangerCaptureLog(models.Model):
    face_id = models.IntegerField(null=True, blank=True)
    uid = models.BigIntegerField()
    time = models.DateTimeField(null=True, blank=True)
    dwfiletype = models.BigIntegerField(null=True, blank=True)
    dwfileindex = models.BigIntegerField(null=True, blank=True)
    dwfilepos = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"UID: {self.uid}, Time: {self.time}"

    def save(self, *args, **kwargs):
        if isinstance(self.time, str) and "/" in self.time:
            self.time = datetime.strptime(self.time, "%Y-%m-%d/%H:%M:%S")
        super(StrangerCaptureLog, self).save(*args, **kwargs)


class ControlLog(models.Model):
    face_id = models.IntegerField(null=True, blank=True)
    uid = models.BigIntegerField()
    name = models.TextField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    cfiletype = models.IntegerField(null=True, blank=True)
    cfileindex = models.IntegerField(null=True, blank=True)
    cfilepos = models.IntegerField(null=True, blank=True)
    similarity = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True)
    extra_info = models.TextField(null=True, blank=True)
    dwfiletype = models.IntegerField(null=True, blank=True)
    dwfileindex = models.IntegerField(null=True, blank=True)
    dwfilepos = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="controllog")
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"

    def save(self, *args, **kwargs):
        if isinstance(self.time, str) and "/" in self.time:
            self.time = datetime.strptime(self.time, "%Y-%m-%d/%H:%M:%S")
        super(ControlLog, self).save(*args, **kwargs)
    class Meta:
            unique_together = ('face_id', 'name', 'time')


import os
import threading
from django.conf import settings
from django.db.models.signals import post_save


@receiver(post_save, sender=ControlLog)
def send_image_after_controllog_save(sender, instance, created, **kwargs):
    if instance.image:
        def async_send():
            try:
                image_path = instance.image.path

                # ✅ Fayl allaqachon mavjudligini tekshiramiz
                if not os.path.exists(image_path):
                    logging.warning(f"⚠️ Rasm topilmadi: {image_path}")
                    return

                # ⚠️ Faylni media/controllog ichida borligini tekshirish
                relative_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
                if relative_path.startswith("controllog/") and os.path.exists(image_path):
                    logging.info(f"🚫 Rasm allaqachon mavjud, yuborilmaydi: {image_path}")
                    return

                send_image_to_controllog(instance.id, image_path)
                logging.info(f"📤 ControlLog rasmi yuborildi: ID={instance.id}, created={created}")
            except Exception as e:
                logging.error(f"❌ ControlLog rasmi yuborishda xatolik (ID={instance.id}): {e}")

        threading.Thread(target=async_send).start()



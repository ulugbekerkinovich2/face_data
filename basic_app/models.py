from django.db import models

class Heartbeat(models.Model):
    device_id = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=50)
    time = models.DateTimeField()

    def __str__(self):
        return f"Heartbeat from Device {self.device_id} at {self.time}"
    class Meta:
        verbose_name_plural = "Heartbeats"
        ordering = ['-time']
        verbose_name = "Heartbeat"


class VerifyPush(models.Model):
    person_id = models.IntegerField()
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

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"


class ICCardInfoPush(models.Model):
    device_id = models.IntegerField()
    ic_card_num = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return f"ICCardInfoPush from Device {self.device_id}"
    
    class Meta:
        verbose_name_plural = "ICCard Info Pushes"
        verbose_name = "ICCard Info Push"


class StrangerCapture(models.Model):
    image_file = models.ImageField(upload_to="stranger_captures/", blank=True, null=True)
    create_time = models.DateTimeField()
    device_id = models.IntegerField()
    direction = models.IntegerField()
    picture_type = models.IntegerField()
    send_in_time = models.IntegerField()
    operator = models.CharField(max_length=50)
    
    def __str__(self):
        return f"StrangerCapture from Device {self.device_id} at {self.create_time}"
    class Meta:
        verbose_name_plural = "Stranger Captures"
        verbose_name = "Stranger Capture"

from django.db import models

class FaceLog(models.Model):
    event_type = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    face_image = models.TextField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.event_type} - {self.user_id or 'Stranger'}"

class RFLog(models.Model):
    event_type = models.CharField(max_length=50)
    card_id = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.event_type} - {self.card_id}"

from django.contrib import admin
from django.utils.html import format_html
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture

@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'time')
    search_fields = ('device_id',)
    list_per_page = 10


@admin.register(VerifyPush)
class VerifyPushAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'name', 'create_time')
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card', 'mj_card_no')
    list_filter = ('create_time',)
    list_per_page = 10


@admin.register(ICCardInfoPush)
class ICCardInfoPushAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
    search_fields = ('device_id', 'ic_card_num')
    list_per_page = 10


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(admin.ModelAdmin):
    list_display = (
        'device_id', 'create_time', 'direction', 
        'operator', 'ip_address', 'thumbnail'
    )
    search_fields = ('device_id', 'operator', 'ip_address')
    list_filter = ('create_time',)
    list_per_page = 10

    def thumbnail(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
                obj.image_file.url
            )
        return "No Image"
    thumbnail.short_description = "Image Preview"
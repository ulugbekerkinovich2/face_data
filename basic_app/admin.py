from django.contrib import admin
from django.utils.html import format_html
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture

@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ip_address', 'mac_address', 'time')
    search_fields = ('device_id', 'ip_address', 'mac_address')
    list_filter = ('time',)

@admin.register(VerifyPush)
class VerifyPushAdmin(admin.ModelAdmin):
    list_display = (
        'person_id', 'name', 'similarity1', 'similarity2', 
        'ip_address', 'create_time'
    )
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card', 'mj_card_no')
    list_filter = ('ip_address', 'create_time', 'verify_type', 'direction')

@admin.register(ICCardInfoPush)
class ICCardInfoPushAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
    search_fields = ('device_id', 'ic_card_num')

# @admin.register(StrangerCapture)
# class StrangerCaptureAdmin(admin.ModelAdmin):
#     list_display = (
#         'device_id', 'create_time', 'direction', 
#         'picture_type', 'operator'
#     )
#     search_fields = ('device_id', 'operator')
#     list_filter = ('create_time', 'direction', 'picture_type')


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(admin.ModelAdmin):
    list_display = (
        'device_id', 'create_time', 'direction', 
        'operator', 'ip_address', 'thumbnail'
    )
    search_fields = ('device_id', 'operator', 'ip_address')
    list_filter = ('create_time', 'direction', 'picture_type')

    def thumbnail(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
                obj.image_file.url
            )
        return "No Image"

    thumbnail.short_description = "Image Preview"
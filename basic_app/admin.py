from django.contrib import admin
from django.utils.html import format_html
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture

# 5 daqiqa
CACHE_TIMEOUT = 60 * 2

@admin.register(Heartbeat)
class HeartbeatAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ip_address', 'mac_address', 'time')
    search_fields = ('device_id', 'ip_address', 'mac_address')
    list_filter = ('time',)
    list_per_page = 20
    @method_decorator(cache_page(CACHE_TIMEOUT))
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context=extra_context)


@admin.register(VerifyPush)
class VerifyPushAdmin(admin.ModelAdmin):
    list_display = (
        'person_id', 'name', 'similarity1', 'similarity2', 
        'ip_address', 'create_time'
    )
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card', 'mj_card_no')
    list_filter = ('ip_address', 'create_time', 'verify_type', 'direction')
    list_per_page = 20
    @method_decorator(cache_page(CACHE_TIMEOUT))
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context=extra_context)


@admin.register(ICCardInfoPush)
class ICCardInfoPushAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
    search_fields = ('device_id', 'ic_card_num')
    list_per_page = 20
    @method_decorator(cache_page(CACHE_TIMEOUT))
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)
    
    @method_decorator(cache_page(CACHE_TIMEOUT))
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context=extra_context)


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(admin.ModelAdmin):
    list_display = (
        'device_id', 'create_time', 'direction', 
        'operator', 'ip_address', 'thumbnail'
    )
    search_fields = ('device_id', 'operator', 'ip_address')
    list_filter = ('create_time', 'direction', 'picture_type')
    list_per_page = 20
    def thumbnail(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
                obj.image_file.url
            )
        return "No Image"
    thumbnail.short_description = "Image Preview"

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def changelist_view(self, request, extra_context=None):
        return super().changelist_view(request, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    @method_decorator(cache_page(CACHE_TIMEOUT))
    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context=extra_context)

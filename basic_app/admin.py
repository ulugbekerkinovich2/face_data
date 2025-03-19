from django.core.cache import cache
import django.db
from django.utils.html import format_html
from django.utils import timezone
from django.contrib import admin
from django.core.cache import cache
import datetime
from .models import Heartbeat, VerifyPush, StrangerCapture, ICCardInfoPush, UsersManagement, ControlLog
from django.utils import timezone
import datetime
from rangefilter.filters import DateRangeFilter
IN_DEVICES = [2489019, 2489007, 2489005, 2488986]
OUT_DEVICES = [2489002, 2489012, 2488993, 2488999]
CACHE_TIMEOUT_SECONDS = 120
class BaseCacheAdmin(admin.ModelAdmin):
    cache_key_prefix = "admin_queryset"
    cache_timeout = 5
    time_field = "created_at"

    def get_queryset(self, request):
        model_name = self.model._meta.model_name
        threshold_date = timezone.now() - datetime.timedelta(days=35)
        cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
        qs = cache.get(cache_key)
        if qs is None:
            qs = super().get_queryset(request).filter(**{f"{self.time_field}__gte": threshold_date})
            cache.set(cache_key, qs, self.cache_timeout)
        return qs

    def movement(self, obj):
        device_id = int(obj.device_id) if obj.device_id else None
        if device_id in IN_DEVICES:
            return format_html('<span style="color: green; font-weight: bold;">IN</span>')
        elif device_id in OUT_DEVICES:
            return format_html('<span style="color: red; font-weight: bold;">OUT</span>')
        return "Unknown"

    movement.short_description = "Movement Direction"


@admin.register(Heartbeat)
class HeartbeatAdmin(BaseCacheAdmin):
    list_display = ('device_id', 'movement', 'ip_address',  'time')
    search_fields = ('device_id',)
    list_per_page = 100
    time_field = "time"


@admin.register(VerifyPush)
class VerifyPushAdmin(BaseCacheAdmin):
    list_display = ('person_id', 'device_id', 'movement', 'name', 'create_time')
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
    list_filter = ('create_time',)
    list_per_page = 100
    time_field = "create_time"


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(BaseCacheAdmin):
    list_display = (
        'device_id', 'movement', 'create_time', 'thumbnail',
    )
    list_filter = ("create_time",)
    search_fields = ('device_id', 'operator', 'ip_address')
    list_per_page = 100
    time_field = "create_time"

    def thumbnail(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" style="height: 135px; width: auto; border-radius: 10px;" />',
                obj.image_file.url
            )
        return "No Image"

    thumbnail.short_description = "Image Preview"


@admin.register(ICCardInfoPush)
class ICCardInfoPushAdmin(BaseCacheAdmin):
    list_display = ('device_id', 'movement', 'ic_card_num', 'created_at', 'ip_address')
    search_fields = ('device_id', 'ic_card_num')
    list_per_page = 100
    time_field = "created_at"

@admin.register(UsersManagement)
class UsersManagementAdmin(admin.ModelAdmin):
    list_display = ('face_id', 'name', 'rf_id_card_num', 'time', 'thumbnail')
    search_fields = ('name', 'rf_id_card_num', 'face_id')
    list_filter = ('face_id',)
    list_per_page = 100
    time_field = "time"

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 100px; width: auto; border-radius: 10px;" />',
                obj.image.url
            )
        return "No Image"

    thumbnail.short_description = "Image"




@admin.register(ControlLog)
class ControlLogAdmin(BaseCacheAdmin):
    list_display = ('id', 'name', 'face_id', 'face_id_status', 'time', 'image_comparison')
    search_fields = ('name', 'face_id', 'uid', 'id')
    list_filter = (('time', DateRangeFilter), 'face_id')
    list_per_page = 200
    ordering = ('-time',)

    def get_queryset(self, request):
        """
        Barcha yozuvlarni olish va queryset’ni 2 daqiqa cache’da saqlash.
        """
        cache_key = "controllog_admin_queryset"
        cached_qs = cache.get(cache_key)
        if cached_qs is not None:
            return cached_qs

        qs = super().get_queryset(request).select_related()  # select_related - optimization
        cache.set(cache_key, qs, CACHE_TIMEOUT_SECONDS)
        return qs

    def face_id_status(self, obj):
        if obj.face_id in IN_DEVICES:
            return format_html('<span style="color:green; font-weight:bold;">IN</span>')
        elif obj.face_id in OUT_DEVICES:
            return format_html('<span style="color:red; font-weight:bold;">OUT</span>')
        return format_html('<span style="color:gray;">UNKNOWN</span>')

    face_id_status.short_description = "Direction"

    def image_comparison(self, obj):
        from basic_app.models import UsersManagement

        user_img_url = ""
        try:
            user = UsersManagement.objects.filter(name=obj.name).first()
            if user and user.image:
                user_img_url = user.image.url
        except:
            pass

        control_img_url = obj.image.url if obj.image else ""

        html = ""

        if user_img_url:
            html += f'<img src="{user_img_url}" width="100" height="100" style="object-fit:cover; border-radius:6px; margin-right:5px;" />'
        else:
            html += '<div style="width:75px;height:75px;display:inline-block;background:#eee;border-radius:6px;line-height:75px;text-align:center;color:#999;font-size:12px;">No User</div>'

        if control_img_url:
            html += f'<img src="{control_img_url}" width="100" height="100" style="object-fit:cover; border-radius:6px; margin-left:5px;" />'
        else:
            html += '<div style="width:75px;height:75px;display:inline-block;background:#fdd;border-radius:6px;line-height:75px;text-align:center;color:#900;font-weight:bold;font-size:12px; margin-left:5px;">Empty</div>'

        return format_html(html)

    image_comparison.short_description = "User vs Log Image"




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
# from rangefilter.filters import DateRangeFilter
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


# @admin.register(Heartbeat)
# class HeartbeatAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'movement', 'ip_address',  'time')
#     search_fields = ('device_id',)
#     list_per_page = 100
#     time_field = "time"


# @admin.register(VerifyPush)
# class VerifyPushAdmin(BaseCacheAdmin):
#     list_display = ('person_id', 'device_id', 'movement', 'name', 'create_time')
#     search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
#     list_filter = ('create_time',)
#     list_per_page = 25
#     time_field = "create_time"


# @admin.register(StrangerCapture)
# class StrangerCaptureAdmin(BaseCacheAdmin):
#     list_display = (
#         'device_id', 'movement', 'create_time', 'thumbnail',
#     )
#     list_filter = ("create_time",)
#     search_fields = ('device_id', 'operator', 'ip_address')
#     list_per_page = 25
#     time_field = "create_time"

#     def thumbnail(self, obj):
#         if obj.image_file:
#             return format_html(
#                 '<img src="{}" style="height: 135px; width: auto; border-radius: 10px;" />',
#                 obj.image_file.url
#             )
#         return "No Image"

#     thumbnail.short_description = "Image Preview"


# @admin.register(ICCardInfoPush)
# class ICCardInfoPushAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'movement', 'ic_card_num', 'created_at', 'ip_address')
#     search_fields = ('device_id', 'ic_card_num')
#     list_per_page = 25
#     time_field = "created_at"

@admin.register(UsersManagement)
class UsersManagementAdmin(admin.ModelAdmin):
    list_display = ('face_id', 'name', 'rf_id_card_num', 'time', 'thumbnail')
    search_fields = ('name', 'rf_id_card_num', 'face_id')
    list_filter = ('face_id',)
    list_per_page = 25
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
    list_filter = ('time', 'face_id')
    list_per_page = 100
    ordering = ('-time',)
    time_field = "time"

    def get_queryset(self, request):
        cache_key = "controllog_admin_queryset_last20days"
        cached_qs = cache.get(cache_key)
        if cached_qs is not None:
            return cached_qs

        cutoff_date = timezone.now() - datetime.timedelta(days=30)
        qs = super().get_queryset(request).filter(time__gte=cutoff_date).only(
            "id", "name", "face_id", "time", "image"
        )
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

        def shrink_img_with_link(url):
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" loading="lazy" width="80" height="80" '
                'style="object-fit:cover;border-radius:5px;filter: blur(0.3px);image-rendering: -webkit-optimize-contrast;" />'
                '</a>',
                url, url
            )

        try:
            user = UsersManagement.objects.only("image").filter(name=obj.name).first()
            user_img = shrink_img_with_link(user.image.url) if user and user.image else None
        except:
            user_img = None

        log_img = shrink_img_with_link(obj.image.url) if obj.image else None

        return format_html(
            '{} {}',
            user_img or '<div style="width:50px;height:50px;background:#eee;border-radius:5px;line-height:50px;text-align:center;color:#777;font-size:10px;display:inline-block;">No User</div>',
            log_img or '<div style="width:50px;height:50px;background:#fdd;border-radius:5px;line-height:50px;text-align:center;color:#900;font-size:10px;font-weight:bold;margin-left:5px;display:inline-block;">Empty</div>'
        )

    image_comparison.short_description = "User vs Log Image"


# from django.core.cache import cache
# from django.utils.html import format_html
# from django.utils import timezone
# from django.contrib import admin
# import datetime
# from .models import (
#     Heartbeat, VerifyPush, StrangerCapture,
#     ICCardInfoPush, UsersManagement, ControlLog
# )

# IN_DEVICES = [2489019, 2489007, 2489005, 2488986]
# OUT_DEVICES = [2489002, 2489012, 2488993, 2488999]
# CACHE_TIMEOUT_SECONDS = 120  # 2 daqiqa


# class BaseCacheAdmin(admin.ModelAdmin):
#     cache_key_prefix = "admin_queryset"
#     cache_timeout = CACHE_TIMEOUT_SECONDS
#     time_field = "created_at"

#     def get_queryset(self, request):
#         model_name = self.model._meta.model_name
#         threshold_date = timezone.now() - datetime.timedelta(days=35)
#         cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date()}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             qs = super().get_queryset(request)
#             if self.time_field:
#                 qs = qs.filter(**{f"{self.time_field}__gte": threshold_date})
#             qs = qs.defer('image') if 'image' in [f.name for f in self.model._meta.fields] else qs
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs

#     def movement(self, obj):
#         device_id = int(obj.device_id) if obj.device_id else None
#         if device_id in IN_DEVICES:
#             return format_html('<span style="color: green; font-weight: bold;">IN</span>')
#         elif device_id in OUT_DEVICES:
#             return format_html('<span style="color: red; font-weight: bold;">OUT</span>')
#         return "Unknown"

#     movement.short_description = "Movement Direction"


# # @admin.register(Heartbeat)
# # class HeartbeatAdmin(BaseCacheAdmin):
# #     list_display = ('device_id', 'movement', 'ip_address', 'time')
# #     search_fields = ('device_id',)
# #     list_per_page = 50
# #     time_field = "time"


# @admin.register(VerifyPush)
# class VerifyPushAdmin(BaseCacheAdmin):
#     list_display = ('person_id', 'device_id', 'movement', 'name', 'create_time')
#     search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
#     list_filter = ('create_time',)
#     list_per_page = 50
#     time_field = "create_time"


# @admin.register(StrangerCapture)
# class StrangerCaptureAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'movement', 'create_time', 'thumbnail')
#     list_filter = ("create_time",)
#     search_fields = ('device_id', 'operator', 'ip_address')
#     list_per_page = 50
#     time_field = "create_time"

#     def thumbnail(self, obj):
#         if obj.image_file:
#             return format_html(
#                 '<img src="{}" style="height: 80px; width: auto; border-radius: 8px; object-fit:cover; filter: blur(0.3px); image-rendering: -webkit-optimize-contrast;" />',
#                 obj.image_file.url
#             )
#         return "No Image"

#     thumbnail.short_description = "Image Preview"


# @admin.register(ICCardInfoPush)
# class ICCardInfoPushAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'movement', 'ic_card_num', 'created_at', 'ip_address')
#     search_fields = ('device_id', 'ic_card_num')
#     list_per_page = 50
#     time_field = "created_at"


# @admin.register(UsersManagement)
# class UsersManagementAdmin(admin.ModelAdmin):
#     list_display = ('face_id', 'name', 'rf_id_card_num', 'time', 'thumbnail')
#     search_fields = ('name', 'rf_id_card_num', 'face_id')
#     list_filter = ('face_id',)
#     list_per_page = 50

#     def thumbnail(self, obj):
#         if obj.image:
#             return format_html(
#                 '<img src="{}" style="height: 60px; width: auto; border-radius: 6px; object-fit:cover; filter: blur(0.3px); image-rendering: -webkit-optimize-contrast;" />',
#                 obj.image.url
#             )
#         return "No Image"

#     thumbnail.short_description = "Image"

# @admin.register(ControlLog)
# class ControlLogAdmin(BaseCacheAdmin):
#     list_display = ('id', 'name', 'face_id', 'face_id_status', 'time', 'image_comparison')
#     search_fields = ('name', 'face_id', 'uid', 'id')
#     list_filter = ('time', 'face_id')
#     list_per_page = 50
#     ordering = ('-time',)
#     time_field = "time"

#     def get_queryset(self, request):
#         cache_key = "controllog_admin_queryset_last20days"
#         cached_qs = cache.get(cache_key)
#         if cached_qs is not None:
#             return cached_qs

#         cutoff_date = timezone.now() - datetime.timedelta(days=30)
#         qs = super().get_queryset(request).filter(time__gte=cutoff_date).only(
#             "id", "name", "face_id", "time", "image"
#         )
#         cache.set(cache_key, qs, CACHE_TIMEOUT_SECONDS)
#         return qs

#     def face_id_status(self, obj):
#         if obj.face_id in IN_DEVICES:
#             return format_html('<span style="color:green; font-weight:bold;">IN</span>')
#         elif obj.face_id in OUT_DEVICES:
#             return format_html('<span style="color:red; font-weight:bold;">OUT</span>')
#         return format_html('<span style="color:gray;">UNKNOWN</span>')

#     face_id_status.short_description = "Direction"

#     def image_comparison(self, obj):
#         from basic_app.models import UsersManagement

#         def shrink_img_with_link(url):
#             return format_html(
#                 '<a href="{}" target="_blank">'
#                 '<img src="{}" loading="lazy" width="50" height="50" '
#                 'style="object-fit:cover;border-radius:5px;filter: blur(0.3px);image-rendering: -webkit-optimize-contrast;" />'
#                 '</a>',
#                 url, url
#             )

#         try:
#             user = UsersManagement.objects.only("image").filter(name=obj.name).first()
#             user_img = shrink_img_with_link(user.image.url) if user and user.image else None
#         except:
#             user_img = None

#         log_img = shrink_img_with_link(obj.image.url) if obj.image else None

#         return format_html(
#             '{} {}',
#             user_img or '<div style="width:50px;height:50px;background:#eee;border-radius:5px;line-height:50px;text-align:center;color:#777;font-size:10px;display:inline-block;">No User</div>',
#             log_img or '<div style="width:50px;height:50px;background:#fdd;border-radius:5px;line-height:50px;text-align:center;color:#900;font-size:10px;font-weight:bold;margin-left:5px;display:inline-block;">Empty</div>'
#         )

#     image_comparison.short_description = "User vs Log Image"

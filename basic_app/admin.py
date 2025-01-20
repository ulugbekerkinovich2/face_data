# # from django.contrib import admin
# # from django.utils.html import format_html
# from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture
# # from django.core.cache import cache

# # class BaseCacheAdmin(admin.ModelAdmin):
# #     """Har bir ModelAdmin uchun keshni sozlab beradigan bazaviy klass."""
# #     cache_key_prefix = "admin_queryset"
# #     cache_timeout = 60  # 60 soniya

# #     def get_queryset(self, request):
# #         # Model nomiga qarab universal cache_key yaratasiz
# #         model_name = self.model._meta.model_name  # masalan, "heartbeat", "verifypush"
# #         cache_key = f"{self.cache_key_prefix}_{model_name}"

# #         qs = cache.get(cache_key)
# #         if qs is None:
# #             qs = super().get_queryset(request)
# #             cache.set(cache_key, qs, self.cache_timeout)
# #         return qs

# #     def save_model(self, request, obj, form, change):
# #         super().save_model(request, obj, form, change)
# #         # Ma'lumot saqlanganda keshni buzib tashlaymiz
# #         model_name = self.model._meta.model_name
# #         cache_key = f"{self.cache_key_prefix}_{model_name}"
# #         cache.delete(cache_key)

# #     def delete_model(self, request, obj):
# #         super().delete_model(request, obj)
# #         # Ma'lumot o'chirilganda ham keshni buzib tashlaymiz
# #         model_name = self.model._meta.model_name
# #         cache_key = f"{self.cache_key_prefix}_{model_name}"
# #         cache.delete(cache_key)

# # @admin.register(Heartbeat)
# # class HeartbeatAdmin(BaseCacheAdmin):
# #     list_display = ('device_id', 'ip_address', 'time')
# #     search_fields = ('device_id',)
# #     list_per_page = 100


# # @admin.register(VerifyPush)
# # class VerifyPushAdmin(BaseCacheAdmin):
# #     list_display = ('person_id', 'name', 'create_time')
# #     search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
# #     list_filter = ('create_time',)
# #     list_per_page = 10
# #     def get_queryset(self, request):
# #         cache_key = "verify_push_queryset_admin"
# #         qs = cache.get(cache_key)
# #         if qs is None:
# #             # Agar keshlanmagan bo'lsa, bazadan tortamiz
# #             qs = super().get_queryset(request)
# #             # Keyin uni 60 soniyaga keshlaymiz
# #             cache.set(cache_key, qs, 60)  
# #         return qs


# # @admin.register(ICCardInfoPush)
# # class ICCardInfoPushAdmin(BaseCacheAdmin):
# #     list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
# #     search_fields = ('device_id', 'ic_card_num')
# #     list_per_page = 100


# # @admin.register(StrangerCapture)
# # class StrangerCaptureAdmin(BaseCacheAdmin):
# #     list_display = (
# #         'device_id', 'create_time', 'direction', 
# #         'operator', 'ip_address', 'thumbnail'
# #     )
# #     search_fields = ('device_id', 'operator', 'ip_address')
# #     list_filter = ('create_time',)
# #     list_per_page = 100

# #     def thumbnail(self, obj):
# #         if obj.image_file:
# #             return format_html(
# #                 '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
# #                 obj.image_file.url
# #             )
# #         return "No Image"
# #     thumbnail.short_description = "Image Preview"

# import datetime
# from django.utils import timezone
# from django.contrib import admin
# from django.core.cache import cache
# from django.utils.html import format_html

# from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture

# class BaseCacheAdmin(admin.ModelAdmin):
#     """
#     Har bir ModelAdmin uchun keshni sozlab beradigan bazaviy klass.
#     get_queryset() override qilinmasa, to'liq jadvalni keshlaydi.
#     """
#     cache_key_prefix = "admin_queryset"
#     cache_timeout = 120  # 120 soniya

#     def get_queryset(self, request):
#         # Default holatda shunchaki jadvalni keshlaymiz (7 kunlik filter hozircha yo'q)
#         model_name = self.model._meta.model_name
#         cache_key = f"{self.cache_key_prefix}_{model_name}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             qs = super().get_queryset(request)
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs

#     def save_model(self, request, obj, form, change):
#         """
#         Ma'lumot saqlanganda keshni buzib tashlaymiz.
#         """
#         super().save_model(request, obj, form, change)
#         model_name = self.model._meta.model_name
#         cache_key = f"{self.cache_key_prefix}_{model_name}"
#         cache.delete(cache_key)

#     def delete_model(self, request, obj):
#         """
#         Ma'lumot o'chirilganda ham keshni buzib tashlaymiz.
#         """
#         super().delete_model(request, obj)
#         model_name = self.model._meta.model_name
#         cache_key = f"{self.cache_key_prefix}_{model_name}"
#         cache.delete(cache_key)


# @admin.register(Heartbeat)
# class HeartbeatAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'ip_address', 'time')
#     search_fields = ('device_id',)
#     list_per_page = 100

#     def get_queryset(self, request):
#         """
#         Oxirgi 7 kunlik ma'lumotni keshlaydi.
#         """
#         model_name = self.model._meta.model_name
#         threshold_date = timezone.now() - datetime.timedelta(days=3)
#         # Kesh kalitiga threshold-ni ham qo'shib, kuniga 1 marta yangilanadigan qilib qo'yamiz
#         cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             # Yangi queryset: so'nggi 7 kunda kelgan yozuvlar
#             qs = super(BaseCacheAdmin, self).get_queryset(request).filter(time__gte=threshold_date)
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs


# @admin.register(VerifyPush)
# class VerifyPushAdmin(BaseCacheAdmin):
#     list_display = ('person_id','device_id', 'name', 'create_time')
#     search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
#     # list_filter = ('create_time',)
#     list_per_page = 100

#     def get_queryset(self, request):
#         model_name = self.model._meta.model_name
#         threshold_date = timezone.now() - datetime.timedelta(days=3)
#         cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             qs = super(BaseCacheAdmin, self).get_queryset(request).filter(create_time__gte=threshold_date)
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs


# @admin.register(ICCardInfoPush)
# class ICCardInfoPushAdmin(BaseCacheAdmin):
#     list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
#     search_fields = ('device_id', 'ic_card_num')
#     list_per_page = 100

#     def get_queryset(self, request):
#         model_name = self.model._meta.model_name
#         threshold_date = timezone.now() - datetime.timedelta(days=3)
#         cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             qs = super(BaseCacheAdmin, self).get_queryset(request).filter(created_at__gte=threshold_date)
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs


# @admin.register(StrangerCapture)
# class StrangerCaptureAdmin(BaseCacheAdmin):
#     list_display = (
#         'device_id', 'create_time', 'direction', 
#         'operator', 'ip_address', 'thumbnail'
#     )
#     search_fields = ('device_id', 'operator', 'ip_address')
#     # list_filter = ('create_time',)
#     list_per_page = 100

#     def get_queryset(self, request):
#         model_name = self.model._meta.model_name
#         threshold_date = timezone.now() - datetime.timedelta(days=3)
#         cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
#         qs = cache.get(cache_key)
#         if qs is None:
#             qs = super(BaseCacheAdmin, self).get_queryset(request).filter(create_time__gte=threshold_date)
#             cache.set(cache_key, qs, self.cache_timeout)
#         return qs

#     def thumbnail(self, obj):
#         if obj.image_file:
#             return format_html(
#                 '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
#                 obj.image_file.url
#             )
#         return "No Image"
#     thumbnail.short_description = "Image Preview"


from django.utils.html import format_html
from django.utils import timezone
from django.contrib import admin
from django.core.cache import cache
import datetime
from .models import Heartbeat, VerifyPush, StrangerCapture, ICCardInfoPush

IN_DEVICES = [2489019, 2489007, 2489005, 2488986]
OUT_DEVICES = [2489002, 2489012, 2488993, 2488999]

class BaseCacheAdmin(admin.ModelAdmin):
    """
    Har bir ModelAdmin uchun oxirgi 3 kunlik ma’lumotni ko‘rsatadigan bazaviy klass.
    """
    cache_key_prefix = "admin_queryset"
    cache_timeout = 5
    time_field = "created_at"  # Default vaqt maydoni

    def get_queryset(self, request):
        """
        Oxirgi 3 kunlik ma’lumotni keshda saqlash va qaytarish.
        """
        model_name = self.model._meta.model_name
        threshold_date = timezone.now() - datetime.timedelta(days=3)
        cache_key = f"{self.cache_key_prefix}_{model_name}_{threshold_date.date().isoformat()}"
        qs = cache.get(cache_key)
        if qs is None:
            qs = super().get_queryset(request).filter(**{f"{self.time_field}__gte": threshold_date})
            cache.set(cache_key, qs, self.cache_timeout)
        return qs

    def movement(self, obj):
        """
        Har bir `device_id` uchun harakat turini ko‘rsatadi.
        """
        device_id = int(obj.device_id) if obj.device_id else None
        if device_id in IN_DEVICES:
            return format_html('<span style="color: green; font-weight: bold;">IN</span>')
        elif device_id in OUT_DEVICES:
            return format_html('<span style="color: red; font-weight: bold;">OUT</span>')
        return "Unknown"

    movement.short_description = "Movement Direction"


@admin.register(Heartbeat)
class HeartbeatAdmin(BaseCacheAdmin):
    list_display = ('device_id', 'ip_address', 'movement', 'time')
    search_fields = ('device_id',)
    list_per_page = 100
    time_field = "time"


@admin.register(VerifyPush)
class VerifyPushAdmin(BaseCacheAdmin):
    list_display = ('person_id', 'device_id', 'movement', 'name', 'create_time')
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
    list_per_page = 100
    time_field = "create_time"


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(BaseCacheAdmin):
    list_display = (
        'thumbnail', 'movement', 'device_id',  'create_time',
        
    )
    search_fields = ('device_id', 'operator', 'ip_address')
    list_per_page = 100
    time_field = "create_time"

    def thumbnail(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" style="height: 70px; width: auto; border-radius: 5px;" />',
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

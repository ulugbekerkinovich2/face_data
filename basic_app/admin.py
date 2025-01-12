from django.contrib import admin
from django.utils.html import format_html
from .models import Heartbeat, VerifyPush, ICCardInfoPush, StrangerCapture
from django.core.cache import cache

class BaseCacheAdmin(admin.ModelAdmin):
    """Har bir ModelAdmin uchun keshni sozlab beradigan bazaviy klass."""
    cache_key_prefix = "admin_queryset"
    cache_timeout = 60  # 60 soniya

    def get_queryset(self, request):
        # Model nomiga qarab universal cache_key yaratasiz
        model_name = self.model._meta.model_name  # masalan, "heartbeat", "verifypush"
        cache_key = f"{self.cache_key_prefix}_{model_name}"

        qs = cache.get(cache_key)
        if qs is None:
            qs = super().get_queryset(request)
            cache.set(cache_key, qs, self.cache_timeout)
        return qs

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Ma'lumot saqlanganda keshni buzib tashlaymiz
        model_name = self.model._meta.model_name
        cache_key = f"{self.cache_key_prefix}_{model_name}"
        cache.delete(cache_key)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # Ma'lumot o'chirilganda ham keshni buzib tashlaymiz
        model_name = self.model._meta.model_name
        cache_key = f"{self.cache_key_prefix}_{model_name}"
        cache.delete(cache_key)

@admin.register(Heartbeat)
class HeartbeatAdmin(BaseCacheAdmin):
    list_display = ('device_id', 'ip_address', 'time')
    search_fields = ('device_id',)
    list_per_page = 10


@admin.register(VerifyPush)
class VerifyPushAdmin(BaseCacheAdmin):
    list_display = ('person_id', 'name', 'create_time')
    search_fields = ('person_id', 'name', 'id_card', 'rfid_card')
    list_filter = ('create_time',)
    list_per_page = 10
    def get_queryset(self, request):
        cache_key = "verify_push_queryset_admin"
        qs = cache.get(cache_key)
        if qs is None:
            # Agar keshlanmagan bo'lsa, bazadan tortamiz
            qs = super().get_queryset(request)
            # Keyin uni 60 soniyaga keshlaymiz
            cache.set(cache_key, qs, 60)  
        return qs


@admin.register(ICCardInfoPush)
class ICCardInfoPushAdmin(BaseCacheAdmin):
    list_display = ('device_id', 'ic_card_num', 'created_at', 'ip_address')
    search_fields = ('device_id', 'ic_card_num')
    list_per_page = 10


@admin.register(StrangerCapture)
class StrangerCaptureAdmin(BaseCacheAdmin):
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
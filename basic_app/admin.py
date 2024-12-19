from django.contrib import admin
from .models import FaceLog, RFLog

@admin.register(FaceLog)
class FaceLogAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user_id', 'name', 'confidence', 'timestamp')
    search_fields = ('user_id', 'name', 'event_type')
    list_filter = ('event_type', 'timestamp')

@admin.register(RFLog)
class RFLogAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'card_id', 'user_id', 'name', 'timestamp')
    search_fields = ('card_id', 'user_id', 'name', 'event_type')
    list_filter = ('event_type', 'timestamp')

from django.urls import path, include
from .views import (
    handle_heartbeat,
    handle_verify_push,
    handle_ic_card_info_push,
    handle_stranger_capture,
    handle_qr_code_push,
    handle_alarm_push,
    update_image_by_id,
    update_image_management
)

urlpatterns = [
    path('Subscribe/heartbeat', handle_heartbeat, name='handle_heartbeat'),
    path('Subscribe/auth', handle_verify_push, name='handle_verify_push'),
    path('Subscribe/RF', handle_ic_card_info_push, name='handle_ic_card_info_push'),
    path('Subscribe/stranger', handle_stranger_capture, name='handle_stranger_capture'),
    path('Subscribe/QRCode', handle_qr_code_push, name='handle_qrcode_push'),
    path('Subscribe/Alarm', handle_alarm_push, name='handle_alarm_push'),
    path('update_image_controllog', update_image_by_id, name='update_image_controllog'),
    path('update_image_management', update_image_management, name='update_image_management'),
]

# if settings.DEBUG:
import debug_toolbar
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
from django.urls import path, include
from .views import (
    handle_heartbeat,
    handle_verify_push,
    handle_ic_card_info_push,
    handle_stranger_capture
)

urlpatterns = [
    path('Subscribe/heartbeat', handle_heartbeat, name='handle_heartbeat'),
    path('Subscribe/auth', handle_verify_push, name='handle_verify_push'),
    path('Subscribe/RF', handle_ic_card_info_push, name='handle_ic_card_info_push'),
    path('Subscribe/stranger', handle_stranger_capture, name='handle_stranger_capture'),
]

# if settings.DEBUG:
import debug_toolbar
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
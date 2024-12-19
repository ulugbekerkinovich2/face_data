from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_subscription, name='auth_subscription'),
    path('stranger/', views.stranger_subscription, name='stranger_subscription'),
    path('rf/', views.rf_subscription, name='rf_subscription'),
]

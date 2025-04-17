from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.billing_info, name='billing_info'),
    path('start_usage/<int:tier_id>/', views.start_usage, name='start_usage'),
    path('stop_usage/<int:usage_id>/', views.stop_usage, name='stop_usage'),
    path('invoice/', views.view_invoice, name='view_invoice'),
    path('payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('subscription/', views.subscription, name='subscription'),
    path('billing_history/', views.billing_history, name='billing_history'),
]

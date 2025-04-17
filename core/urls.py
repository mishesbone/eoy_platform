from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('join-waitlist/', views.join_waitlist, name='join_waitlist'),
    path('monitor-gpu/', views.trigger_gpu_monitoring, name='monitor_gpu'),
    path('billing-check/', views.trigger_billing_check, name='billing_check'),
    path('task-status/<str:task_id>/', views.check_task_status, name='task_status'),
]

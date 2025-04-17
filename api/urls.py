from django.urls import path
from . import views

urlpatterns = [
    path('submit_task/', views.api_submit_task, name='api_submit_task'),
    path('task_status/<int:task_id>/', views.api_task_status, name='api_task_status'),
]

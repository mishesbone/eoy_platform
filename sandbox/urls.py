from django.urls import path
from . import views

urlpatterns = [
    path('', views.sandbox_home, name='sandbox_home'),
    path('submit_task/', views.submit_task, name='submit_task'),
    path('task_status/<int:task_id>/', views.task_status, name='task_status'),
    path('', views.submit_sandbox_task, name='sandbox_home'),

]



urlpatterns = [
    
]

# filepath: c:\Users\CSO-II\Documents\mishes projects\eoy_platform\jobs\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_job, name='submit_job'),
    path('view/', views.view_jobs, name='view_jobs'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('update/<int:job_id>/', views.update_job, name='update_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),]
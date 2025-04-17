# filepath: c:\Users\CSO-II\Documents\mishes projects\eoy_platform\dashboard\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_home'),  # Dashboard home view
]
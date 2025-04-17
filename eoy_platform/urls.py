# filepath: c:\Users\CSO-II\Documents\mishes projects\eoy_platform\eoy_platform\urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Home page and landing
    path('dashboard/', include('dashboard.urls')),  # Dashboard for users
    path('jobs/', include('jobs.urls')),  # Job management and task tracking
    path('billing/', include('billing.urls')),  # Billing management
    path('auth/', include('auth.urls')),  # Authentication routes
    path('api/', include('api.urls')),  # API endpoints
    path('sandbox/', include('sandbox.urls')),  # AI sandbox management
]
from django.contrib import admin
from .models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'user', 'status', 'created_at')
    search_fields = ('job_name', 'user__username')
    list_filter = ('status',)

admin.site.register(Job, JobAdmin)

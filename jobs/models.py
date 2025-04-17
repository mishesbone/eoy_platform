from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    job_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Job: {self.job_name} (Status: {self.status})"

    def mark_completed(self, result=None):
        self.status = 'completed'
        self.result = result
        self.save()

    def mark_failed(self, error_message=None):
        self.status = 'failed'
        self.result = error_message
        self.save()

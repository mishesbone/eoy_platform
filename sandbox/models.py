from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('processing', 'Processing'), ('completed', 'Completed')], default='submitted')
    result = models.TextField(null=True, blank=True)  # Result will be populated once processing is done
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

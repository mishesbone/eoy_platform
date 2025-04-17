from django.db import models
from django.contrib.auth.models import User

# Define possible billing tiers
class BillingTier(models.Model):
    name = models.CharField(max_length=50)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)  # Price per hour of usage
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - ${self.price_per_hour}/hr"

# Resource usage tracking for each user
class ResourceUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billing_tier = models.ForeignKey(BillingTier, on_delete=models.SET_NULL, null=True)
    usage_start_time = models.DateTimeField(auto_now_add=True)
    usage_end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Usage for {self.user.username} - {self.billing_tier.name}"

    def calculate_cost(self):
        """Calculates the cost based on usage and billing tier price."""
        if self.usage_end_time:
            usage_duration = self.usage_end_time - self.usage_start_time
            total_hours = usage_duration.total_seconds() / 3600
            self.total_cost = total_hours * self.billing_tier.price_per_hour
            self.save()

# Invoicing model to track completed usage and bills
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Overdue', 'Overdue'),
    ('Cancelled', 'Cancelled'),]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return f"Invoice #{self.id} for {self.user.username}"

class BillingRecord(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.amount}"

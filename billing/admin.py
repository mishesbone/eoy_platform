from django.contrib import admin
from .models import BillingTier, ResourceUsage, Invoice, BillingRecord

# Register the BillingRecord model


admin.site.register(BillingTier)
admin.site.register(ResourceUsage)
admin.site.register(Invoice)
admin.site.register(BillingRecord)


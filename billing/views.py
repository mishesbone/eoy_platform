from django.shortcuts import render
from django.http import JsonResponse
from .models import BillingTier, ResourceUsage, Invoice
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# View to display billing info and available tiers
@login_required
def billing_info(request):
    billing_tiers = BillingTier.objects.all()
    user_usage = ResourceUsage.objects.filter(user=request.user, usage_end_time=None).first()

    # If the user is currently using resources, show current usage details
    if user_usage:
        user_usage_duration = timezone.now() - user_usage.usage_start_time
        user_usage_total_cost = user_usage_duration.total_seconds() / 3600 * user_usage.billing_tier.price_per_hour
    else:
        user_usage_total_cost = 0.00

    return render(request, 'billing/billing_info.html', {
        'billing_tiers': billing_tiers,
        'user_usage_total_cost': user_usage_total_cost
    })

# View to display and track resource usage
@login_required
def start_usage(request, tier_id):
    billing_tier = BillingTier.objects.get(id=tier_id)

    # Create a new resource usage record for the user
    usage = ResourceUsage.objects.create(user=request.user, billing_tier=billing_tier)

    return JsonResponse({"status": "success", "message": "Resource usage started", "usage_id": usage.id})

# View to stop usage and generate an invoice
@login_required
def stop_usage(request, usage_id):
    usage = ResourceUsage.objects.get(id=usage_id)
    usage.usage_end_time = timezone.now()
    usage.calculate_cost()  # Calculate the total cost based on usage time
    usage.save()

    # Generate an invoice for the user
    invoice = Invoice.objects.create(
        user=request.user,
        total_amount=usage.total_cost,
        due_date=timezone.now() + timezone.timedelta(days=30)  # 30 days due date
    )

    return JsonResponse({"status": "success", "message": "Usage stopped, invoice generated", "invoice_id": invoice.id})

# View to view user's past invoices

@login_required
def view_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invoice not found."})

    return render(request, 'invoice_detail.html', {'invoice': invoice})


#billing history
@login_required
def billing_history(request):
    """
    Displays the billing history for the logged-in user.
    """
    user = request.user  # Get the currently logged-in user
    invoices = Invoice.objects.filter(user=user)  # Get all invoices for this user

    return render(request, 'billing/billing_history.html', {'invoices': invoices, 'user': user})

@login_required
def payment_history(request):
    """
    Displays the payment history for the logged-in user.
    """
    user = request.user  # Get the currently logged-in user
    invoices = Invoice.objects.filter(user=user)  # Get all invoices for this user
    payments = []
    for invoice in invoices:
        payments.append({
            'invoice': invoice,
            'payment_status': invoice.payment_status,
            'payment_date': invoice.payment_date,
        })

    return render(request, 'billing/payment_history.html', {'payments': payments, 'user': user})

from django.shortcuts import redirect
from django.contrib import messages

@login_required
def process_payment(request, invoice_id):
    """
    Processes the payment for a specific invoice.
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        messages.error(request, "Invoice not found.")
        return redirect('billing:payment_failure')

    try:
        # Simulate payment processing (replace this with real API logic if needed)
        payment_successful = True  # This could be the result of an API call

        if payment_successful:
            invoice.payment_status = 'Paid'
            invoice.payment_date = timezone.now()
            invoice.save()

            messages.success(request, "Payment processed successfully.")
            return redirect('billing:payment_success')
        else:
            messages.error(request, "Payment failed. Please try again.")
            return redirect('billing:payment_failure')

    except Exception as e:
        print(f"[ERROR] Payment processing failed: {e}")
        messages.error(request, "An unexpected error occurred during payment.")
        return redirect('billing:payment_failure')


from django.contrib import messages
from .models import Invoice

@login_required
def payment_success(request):
    """
    Displays a success message and details of the latest invoice after payment processing.
    """
    # Get the latest invoice for the user
    latest_invoice = Invoice.objects.filter(user=request.user).order_by('-payment_date').first()

    if latest_invoice:
        messages.success(request, f"Payment for Invoice #{latest_invoice.id} was successful.")
    else:
        messages.success(request, "Payment was successful.")

    return render(request, 'billing/payment_success.html', {
        'invoice': latest_invoice
    })

from django.contrib import messages

@login_required
def payment_failure(request):
    """
    Displays an error message after payment processing failure.
    """
    messages.error(request, "Payment failed. Please try again or contact support if the issue persists.")

    return render(request, 'billing/payment_failure.html')


@login_required
def subscription(request):
    """
    Displays the subscription details for the logged-in user.
    """
    user = request.user
    billing_tiers = BillingTier.objects.all()
    
    # Check if the user currently has an active resource usage
    active_usage = ResourceUsage.objects.filter(user=user, usage_end_time=None).first()
    
    current_subscription = {
        'tier': active_usage.billing_tier if active_usage else None,
        'start_time': active_usage.usage_start_time if active_usage else None,
    }

    return render(request, 'billing/subscription.html', {
        'billing_tiers': billing_tiers,
        'current_subscription': current_subscription,
        'user': user
    })

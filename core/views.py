from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from celery.result import AsyncResult
from .models import WaitlistEntry
from gpu_monitor.consumer import monitor_gpu_usage, check_and_report_resource_usage

# Define services and pricing
SERVICES = [
    {"name": "Bare-metal GPU Leasing", "desc": "Access dedicated high-performance compute nodes."},
    {"name": "Hosted LLM Training", "desc": "Train your foundation or fine-tuned models on demand."},
    {"name": "Real-Time Inference API", "desc": "Low-latency endpoints for LLMs and diffusion models."},
    {"name": "Private AI Sandboxes", "desc": "Secure containers for internal enterprise AI workloads."},
]

PRICING = [
    {"tier": "Starter", "price": "$0.50/hr", "features": ["NVIDIA T4", "2vCPU", "4GB RAM"]},
    {"tier": "Pro", "price": "$2.00/hr", "features": ["NVIDIA A100", "8vCPU", "64GB RAM"]},
    {"tier": "Enterprise", "price": "Custom", "features": ["Multi-GPU", "Private Cluster", "SLAs"]},
]

def landing_page(request):
    mock_gpu_status = {
        "NVIDIA T4": {"available": 14, "total": 20},
        "NVIDIA A100": {"available": 2, "total": 4},
        "RTX 4090": {"available": 0, "total": 3},
    }
    return render(request, 'landing.html', {
        'services': SERVICES,
        'pricing': PRICING,
        'gpu_status': mock_gpu_status
    })

@csrf_exempt
def join_waitlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if name and email:
            WaitlistEntry.objects.get_or_create(name=name, email=email)
            send_mail(
                'Waitlist Confirmation',
                f'Hello {name},\nYou have successfully joined the waitlist.',
                'noreply@eoyplatform.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "Missing fields"})
    return JsonResponse({"status": "invalid method"})

def trigger_gpu_monitoring(request):
    result = monitor_gpu_usage.apply_async()
    return JsonResponse({"status": "Monitoring started", "task_id": result.id})

def trigger_billing_check(request):
    result = check_and_report_resource_usage.apply_async()
    return JsonResponse({"status": "Billing check started", "task_id": result.id})

def check_task_status(request, task_id):
    result = AsyncResult(task_id)
    return JsonResponse({
        "status": result.status,
        "result": result.result if result.ready() else None
    })

# views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from jobs.models import Job
from jobs.tasks import run_ai_task  # Import the Celery task
from billing.models import BillingRecord  # Assuming you have a BillingRecord model
from django.contrib.auth.decorators import login_required


def dashboard(request):
    if request.method == 'POST':
        # Handling form submission for new job
        job_name = request.POST.get('job_name')
        job_description = request.POST.get('job_description')
        
        # Create and save a new Job
        job = Job(job_name=job_name, job_description=job_description, status='Pending', created_at=timezone.now())
        job.save()

        # Run the AI task asynchronously via Celery
        run_ai_task.delay(job.id)

        return redirect('dashboard')  # Redirect to avoid resubmission on refresh

    # Fetch recent jobs and billing summary
    recent_jobs = Job.objects.order_by('-created_at')[:5]  # Get the latest 5 jobs
    billing_summary = BillingRecord.objects.order_by('-timestamp')[:5]  # Get the latest 5 billing records

    return render(request, 'dashboard/template/dashboard.html', {
        'recent_jobs': recent_jobs,
        'billing_summary': billing_summary,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Job
from django.contrib.auth.decorators import login_required
from jobs.tasks import run_ai_task

@login_required
def submit_job(request):
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
        job_description = request.POST.get('job_description')

        if job_name and job_description:
            job = Job.objects.create(user=request.user, job_name=job_name, job_description=job_description)
            # Simulate some task completion logic here (e.g., async task or processing)
            job.mark_completed(result="Job completed successfully.")
            return JsonResponse({"status": "success", "message": f"Job {job_name} submitted successfully!"})

        return JsonResponse({"status": "error", "message": "Please provide job name and description."})

    return render(request, 'jobs/submit_job.html')

@login_required
def view_jobs(request):
    jobs = Job.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'jobs/view_jobs.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id, user=request.user)
        return render(request, 'jobs/job_detail.html', {'job': job})
    except Job.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Job not found."}, status=404)


def create_and_run_job(user, name, description):
    job = Job.objects.create(user=user, job_name=name, job_description=description)
    run_ai_task.delay(job.id)

def get_job_status(job_id):
    try:
        job = Job.objects.get(id=job_id)
        return {
            "job_id": job.id,
            "status": job.status,
            "result": job.result if job.status == 'completed' else "Processing..."
        }
    except Job.DoesNotExist:
        return {"status": "error", "message": "Job not found."}
    


@login_required
def update_job(request, job_id):
    """
    Updates the details of a specific job.
    """
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        job_name = request.POST.get('job_name', job.job_name)
        job_description = request.POST.get('job_description', job.job_description)

        job.job_name = job_name
        job.job_description = job_description
        job.save()

        return JsonResponse({"status": "success", "message": "Job updated successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

@login_required
def delete_job(request, job_id):
    """
    Deletes a specific job.
    """
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        job.delete()
        return JsonResponse({"status": "success", "message": "Job deleted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request method."})
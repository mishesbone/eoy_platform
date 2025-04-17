from django.shortcuts import render
from django.http import JsonResponse
from .tasks import submit_task_to_agent, get_task_status
from .models import Task
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from jobs.tasks import run_ai_task

def sandbox_home(request):
    """
    Displays the sandbox page with options to submit a task, view the task list, and check statuses.
    """
    tasks = Task.objects.all()  # Fetch all tasks from the database
    return render(request, 'sandbox/sandbox.html', {'tasks': tasks})

def submit_task(request):
    """
    Handles task submission. Starts a new task in the background and returns the task ID.
    """
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        
        if not task_name or not task_description:
            return JsonResponse({"status": "error", "message": "Task name and description are required."})
        
        # Create a new task in the database
        task = Task.objects.create(
            name=task_name,
            description=task_description,
            status='submitted'
        )
        
        # Submit task to the agent framework for processing
        submit_task_to_agent(task)
        
        return JsonResponse({"status": "success", "task_id": task.id})

@login_required
def submit_sandbox_task(request):
    if request.method == 'POST':
        job_name = request.POST.get('job_name', 'Untitled Job')
        job_description = request.POST.get('job_description', 'No description')
        job = Job.objects.create(user=request.user, job_name=job_name, job_description=job_description)
        run_ai_task.delay(job.id)
        return redirect('dashboard_home')
    
    return render(request, 'sandbox.html')

def task_status(request, task_id):
    """
    Returns the status of a specific task.
    """
    task = Task.objects.get(id=task_id)
    return JsonResponse({"task_id": task.id, "status": task.status, "result": task.result})

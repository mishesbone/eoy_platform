from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sandbox.tasks import submit_task_to_agent, get_task_status 
from sandbox.models import Task

@csrf_exempt
def api_submit_task(request):
    """
    API endpoint to submit a task to the agent framework. 
    Expects task name and description in the POST body.
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

@csrf_exempt
def api_task_status(request, task_id):
    """
    API endpoint to check the status of a specific task.
    Returns the task status and result.
    """
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Task not found."})

    return JsonResponse({
        "task_id": task.id,
        "status": task.status,
        "result": task.result if task.status == 'completed' else "Processing..."
    })

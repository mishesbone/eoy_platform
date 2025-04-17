# filepath: c:\Users\CSO-II\Documents\mishes projects\eoy_platform\sandbox\tasks.py
from celery import shared_task
from .models import Task

@shared_task
def submit_task_to_agent(task):
    """
    Simulates submitting a task to an agent for processing.
    """
    task.status = 'processing'
    task.save()

    # Simulate task processing (replace with actual logic)
    task.result = f"Processed task: {task.name}"
    task.status = 'completed'
    task.save()

@shared_task
def get_task_status(task_id):
    """
    Retrieves the status of a task.
    """
    try:
        task = Task.objects.get(id=task_id)
        return {"status": task.status, "result": task.result}
    except Task.DoesNotExist:
        return {"status": "error", "message": "Task not found."}
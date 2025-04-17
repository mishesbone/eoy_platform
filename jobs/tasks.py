
from celery import shared_task
from jobs.models import Job
import time
import traceback

@shared_task
def perform_job(job_id):
    try:
        # Simulate job processing logic
        job = Job.objects.get(id=job_id)
        job.status = 'in_progress'
        job.save()

        # Simulate task completion (e.g., model training, processing)
        result = "Job completed successfully!"

        # Mark job as completed with result
        job.mark_completed(result=result)

    except Job.DoesNotExist:
        print(f"Job with ID {job_id} not found.")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        job.mark_failed(error_message=str(e))


@shared_task
def run_ai_task(job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.status = 'in_progress'
        job.save()

        # Simulate workload (replace with actual AI/LLM processing logic)
        time.sleep(10)

        result_output = f"Simulated processing complete for: {job.job_name}"
        job.mark_completed(result=result_output)
        return result_output

    except Job.DoesNotExist:
        return f"Job with ID {job_id} does not exist."

    except Exception as e:
        error_details = f"Error: {str(e)}\n{traceback.format_exc()}"
        if 'job' in locals():
            job.mark_failed(error_message=error_details)
        return error_details


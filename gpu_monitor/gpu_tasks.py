from celery import shared_task
import subprocess
import json
import datetime
import logging

logger = logging.getLogger(__name__)

@shared_task
def monitor_gpu_usage():
    print("Monitoring GPU usage...")
    try:
        # Sample using `nvidia-smi` to get GPU stats in JSON format (requires compatible NVIDIA driver)
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu,memory.used,memory.total', '--format=csv,nounits,noheader'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        output = result.stdout.strip()
        if output:
            utilization, memory_used, memory_total = output.split(", ")
            log_message = (
                f"[{datetime.datetime.now()}] GPU Utilization: {utilization}%, "
                f"Memory Used: {memory_used} MiB / {memory_total} MiB"
            )
            print(log_message)
            logger.info(log_message)
        else:
            logger.warning("No output from nvidia-smi.")

    except Exception as e:
        logger.error(f"Error monitoring GPU usage: {str(e)}")
        print(f"Error monitoring GPU usage: {str(e)}")


@shared_task
def check_and_report_resource_usage():
    print("Checking and reporting resource usage...")
    try:
        # Simulated logic: check if GPU usage exceeds a threshold
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,nounits,noheader'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        usage_str = result.stdout.strip()
        usage = int(usage_str) if usage_str else 0

        if usage > 80:
            warning_msg = f"⚠️ High GPU usage detected: {usage}%"
            print(warning_msg)
            logger.warning(warning_msg)
        else:
            normal_msg = f"✅ GPU usage is normal: {usage}%"
            print(normal_msg)
            logger.info(normal_msg)

    except Exception as e:
        logger.error(f"Error checking GPU resource usage: {str(e)}")
        print(f"Error checking GPU resource usage: {str(e)}")

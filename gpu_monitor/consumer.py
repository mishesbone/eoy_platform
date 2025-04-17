# gpu_monitor/consumer.py
# -*- coding: utf-8 -*-
import time
import json
import redis
import GPUtil
from celery import shared_task  # ✅ FIXED
from django.conf import settings

# Redis client setup
redis_client = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True
)

@shared_task(bind=True, max_retries=3)
def monitor_gpu_usage(self):
    """
    Celery task to monitor GPU usage and store it in Redis.
    """
    try:
        gpus = GPUtil.getGPUs()
        gpu_data = {}

        for gpu in gpus:
            gpu_data[gpu.id] = {
                'name': gpu.name,
                'memory_used': gpu.memoryUsed,
                'memory_total': gpu.memoryTotal,
                'memory_free': gpu.memoryFree,
                'utilization': round(gpu.load * 100, 2),  # ✅ FIXED to get actual % load
                'temperature': gpu.temperature
            }

        timestamp = int(time.time())
        gpu_data['timestamp'] = timestamp
        redis_client.set(f'gpu_usage:{timestamp}', json.dumps(gpu_data))

        print(f"✅ GPU Usage at {timestamp}: {gpu_data}")
        return f"Successfully recorded GPU usage at {timestamp}"

    except Exception as e:
        print(f"❌ Error monitoring GPU usage: {e}")
        raise self.retry(exc=e)


@shared_task(bind=True, max_retries=3)
def check_and_report_resource_usage(self):
    """
    Celery task to check GPU usage from Redis and simulate billing based on utilization.
    """
    try:
        keys = redis_client.keys('gpu_usage:*')
        if not keys:
            return "No GPU usage data found."

        latest_key = max(keys, key=lambda k: int(k.split(':')[-1]))
        gpu_data = json.loads(redis_client.get(latest_key))
        print(f"🔍 GPU data for billing: {gpu_data}")

        for gpu_id, stats in gpu_data.items():
            if gpu_id == 'timestamp':
                continue

            if stats['utilization'] > 80:
                print(f"⚠️ High GPU usage on {stats['name']} (ID: {gpu_id}). Billing triggered.")
                redis_client.set(f'billing_log:{gpu_id}:{gpu_data["timestamp"]}', json.dumps(stats))

        return "✅ Resource usage and billing check completed."

    except Exception as e:
        print(f"❌ Error checking resource usage: {e}")
        raise self.retry(exc=e)


def get_last_gpu_usage():
    """
    Fetch the latest GPU usage data from Redis.
    """
    keys = redis_client.keys('gpu_usage:*')
    if not keys:
        return None

    latest_key = max(keys, key=lambda k: int(k.split(':')[-1]))
    return json.loads(redis_client.get(latest_key))


def debug_gpu_monitor():
    """
    Print current GPU stats without Celery (for testing).
    """
    try:
        gpus = GPUtil.getGPUs()
        gpu_data = {}

        for gpu in gpus:
            gpu_data[gpu.id] = {
                'name': gpu.name,
                'memory_used': gpu.memoryUsed,
                'memory_total': gpu.memoryTotal,
                'memory_free': gpu.memoryFree,
                'utilization': round(gpu.load * 100, 2),  # ✅ FIXED
                'temperature': gpu.temperature
            }

        print(f"🛠️ GPU Monitor Debug Data: {gpu_data}")
        return gpu_data

    except Exception as e:
        print(f"❌ Error in GPU monitor debug mode: {e}")


if __name__ == "__main__":
    debug_gpu_monitor()

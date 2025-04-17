# EOY Platform

EOY Platform is a Django-based project designed to monitor GPU usage, manage tasks, and handle billing for resource usage.

## Features
- **GPU Monitoring**: Tracks GPU usage and stores data in Redis.
- **Task Management**: Submit and track tasks using Celery workers.
- **Billing System**: Manage resource usage, generate invoices, and process payments.

## Requirements
- Python 3.10+
- Django 4.x
- MySQL 8.x
- Redis
- Celery

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/eoy_platform.git
   cd eoy_platform
2. Create and activate a virtual environment:
    python -m venv venv
    venv\Scripts\activate  # On Windows

3. Install dependencies:
    pip install -r requirements.txt
4. Configure the database in settings.py:

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eoy',  # Database name
        'USER': 'admin',  # Username
        'PASSWORD': 'admin',  # Password
        'HOST': 'localhost',  # Host
        'PORT': '3306',  # Port
        }
    }

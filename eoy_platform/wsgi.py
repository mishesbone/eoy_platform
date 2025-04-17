# filepath: c:\Users\CSO-II\Documents\mishes projects\eoy_platform\eoy_platform\wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eoy_platform.settings')

application = get_wsgi_application()
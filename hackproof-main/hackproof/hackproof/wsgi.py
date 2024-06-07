"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import threading

from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ObjectDoesNotExist
from polls.models import Path  # replace "polls" with the name of your app
from log_files.logs import start_logging

def start_logging_in_thread():
    log_file = "folder_access"  # Change this to your desired log file path
    path_obj = Path.objects.first()
    folder_to_watch = path_obj.path if path_obj else "C:/Users"
    start_logging(log_file, folder_to_watch)


logging_thread = threading.Thread(target=start_logging_in_thread)
logging_thread.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .logs import start_logging
from polls.models import Path

def start_logging_view(request):
    log_file = "folder_access"  # Change this to your desired log file path
    folder_to_watch = Path.objects.first()
    current_path = folder_to_watch.path
     # Replace with your folder path (be cautious)
    start_logging(log_file, current_path)
    return HttpResponse("Logging has started")
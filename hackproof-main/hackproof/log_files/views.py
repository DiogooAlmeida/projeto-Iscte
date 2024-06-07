from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .logs import start_logging

def start_logging_view(request):
    log_file = "folder_access"  # Change this to your desired log file path
    folder_to_watch = "C:/Users/ruiaq/Downloads"  # Replace with your folder path (be cautious)
    start_logging(log_file, folder_to_watch)
    return HttpResponse("Logging has started")
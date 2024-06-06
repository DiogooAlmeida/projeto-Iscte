import os
import time
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone

class LogCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log_date = time.strftime("%Y-%m-%d")
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Construct the path to the log file
        log_file_path = os.path.join(script_dir, f"watchdog/folder_access_{log_date}.log")

        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as logfile:
                new_logs = [line.strip().split(' - ', 4) for line in logfile if len(line.strip().split(' - ', 4)) == 5]
                # Get the previous logs from the cache
                previous_logs = cache.get('logs', [])
                if previous_logs and new_logs != previous_logs:
                    now = timezone.now()
                    messages.info(request, 'Possível intruso detetado, verifique os logs.')
                logs = [{"date_time": parts[0], "event_name": parts[1], "path": parts[2], "destination_path": parts[3], "user": parts[4]} for parts in new_logs]
                # Store the new logs in the cache
                cache.set('logs', logs)

        response = self.get_response(request)

        return response
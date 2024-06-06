import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import getpass
import os

class FolderMonitor(PatternMatchingEventHandler):
    def __init__(self, log_file):
        log_date = time.strftime("%Y-%m-%d")
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the log file name
        self.log_file = os.path.join(script_dir, f"{log_file}_{log_date}")
        super().__init__(ignore_patterns=[log_file, "*.tmp"])

    def on_any_event(self, event):
        if event.is_directory:
            return None

        event_name = event.__class__.__name__
        log_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Get destination path for move events
        dest_path = event.dest_path if hasattr(event, 'dest_path') else 'N/A'
        if dest_path == '':
            dest_path = 'N/A'
        # Get current user
        user = getpass.getuser()

        # Write to log file
        with open(f"{self.log_file}.log", "a") as f:
            f.write(f"{log_time} - {event_name} - {event.src_path} - {dest_path} - {user}\n")

if __name__ == "__main__":
    log_file = "folder_access"  # Change this to your desired log file path
    folder_to_watch = "C:/Users/ruiaq/Downloads"  # Replace with your folder path (be cautious)
    print("Logging is active")
    event_handler = FolderMonitor(log_file)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import getpass
import os
from cryptography.fernet import Fernet

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

    # Get the filename of the log file
    log_filename = os.path.basename(self.log_file)

    # Ensure the log folder exists
    os.makedirs('log_folder', exist_ok=True)

    # Prepare the log entry
    log_entry = f"{log_time} - {event_name} - {event.src_path} - {dest_path} - {user}\n"

    # Retrieve the key from the environment variable
    key = os.environ['FERNET_KEY'].encode()

    # Encrypt the log entry
    encrypted_log_entry = encrypt_data(key, log_entry)

    # Write the encrypted log entry to the file
    with open(f"log_folder\\{log_filename}.log", "ab") as f:
        f.write(encrypted_log_entry)

def start_logging(log_file, folder_to_watch):
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

def encrypt_data(key, data):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

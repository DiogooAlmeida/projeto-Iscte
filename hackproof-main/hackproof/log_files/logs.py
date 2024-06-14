import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import getpass
import os
from .encrypt import encrypt_files, decrypt_files
import threading

# Classe que monitoriza a pasta por mudanças
class FolderMonitor(PatternMatchingEventHandler):

    # Construtor da classe
    def __init__(self, log_file):
        encrypt_files()
        log_date = time.strftime("%Y-%m-%d")
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Join the script directory with the log file name
        self.log_file = os.path.join(script_dir, f"{log_file}_{log_date}")
        super().__init__(ignore_patterns=[log_file, "*.tmp"])

    # Método que é chamado quando ocorre um evento
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
    
        # Write to log file
        with open(f"log_folder\\{log_filename}.log", "a") as f:
            f.write(f"{log_time} - {event_name} - {event.src_path} - {dest_path} - {user}\n")

# Função que inicia o log
def start_logging(log_file, folder_to_watch):
    event_handler = FolderMonitor(log_file)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)
    observer.start()

    # Start a new thread that encrypts files every 24 hours
    def encrypt_every_day():
        while True:
            time.sleep(86400)  # Sleep for 24 hours
            encrypt_files()

    encrypt_thread = threading.Thread(target=encrypt_every_day)
    encrypt_thread.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import time
import os
import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from zoneinfo import ZoneInfo

home_dir = Path.home()

size_handler = RotatingFileHandler(
    os.path.join(home_dir, 'wrapper.log'), maxBytes=10485760, backupCount=5, encoding='utf-8'
)

formatter = logging.Formatter("%(asctime)s -%(processName)s - %(threadName)s - %(levelname)s - %(message)s")
size_handler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
# Get logger and add handlers
logger = logging.getLogger()
logger.addHandler(size_handler)
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)



# Assuming your login function is defined in login_module.py
from login_module import login_function

def reload_module(module_name):
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    else:
        importlib.import_module(module_name)

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            module_name = os.path.basename(event.src_path)[:-3]
            print(f'{module_name} has been modified, reloading...')
            reload_module(module_name)

def main():
    # Perform login
    login_function()
    print("Login successful!")

    # Path to monitor
    path = "."  # Directory to watch
    
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
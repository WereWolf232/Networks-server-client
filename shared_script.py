# should probably git.ignore this
# but for now i'll keep it for future reference

import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('shared.py'):
            dest_path = './server/shared.py'
            shutil.copy(event.src_path, dest_path)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./client', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

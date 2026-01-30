import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from log_tools.parser import parse_line, save_to_csv
from log_tools.detector import Detector


LOG_FILE = "/logs/collected.log"

class LogWatcher(FileSystemEventHandler):
    def __init__(self, filepath):
        print("[*] Started new log detection in collected.log")
        self.filepath = filepath
        self._position = 0
        self.detector = Detector()

        # set the starting position at the end of a file (not analyzing old traffic)
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                f.seek(0, os.SEEK_END)
                self._position = f.tell()

    def on_modified(self, event):
        if event.src_path != self.filepath:
            return

        with open(self.filepath, "r") as f:
            f.seek(self._position)
            new_lines = f.readlines()
            self._position = f.tell()

        for line in new_lines:
            self.process_line(line.strip())

    def process_line(self, line):
        if not line:
            return

        parsed_log = parse_line(line)

        if parsed_log is None:
            return

        save_to_csv(parsed_log)
        self.detector.run_all(parsed_log)


if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        print(f"[!] File {LOG_FILE} does not exist.")
        exit(1)

    print(f"[*] Monitoring {LOG_FILE}...")

    event_handler = LogWatcher(LOG_FILE)
    observer = Observer()
    observer.schedule(event_handler, path="/logs", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

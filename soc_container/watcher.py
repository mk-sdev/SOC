import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from parser import parse_line, save_to_csv


LOG_FILE = "/logs/collected.log"

class LogWatcher(FileSystemEventHandler):
    def __init__(self, filepath):
        self.filepath = filepath
        self._position = 0

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

        print(f"[NEW LOG] {line}")

        df = parse_line(line)

        if df is None:
            return
        else:
            save_to_csv(df)

        # print("\n[PARSED LOG]")
        # print(df.to_string(index=False))

        #TODO:
        # - detection
        # - alerting


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

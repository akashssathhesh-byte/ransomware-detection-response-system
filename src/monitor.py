from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RansomwareEventHandler(FileSystemEventHandler):
    def __init__(self, detector, alert_manager, response_manager):
        self.detector = detector
        self.alert_manager = alert_manager
        self.response_manager = response_manager

    def _process(self, event_type, path):
        if not path or Path(path).is_dir():
            return

        alert = self.detector.record(event_type, path)
        if alert:
            self.alert_manager.emit(alert)
            self.response_manager.handle(alert)

    def on_created(self, event):
        self._process("created", event.src_path)

    def on_modified(self, event):
        self._process("modified", event.src_path)

    def on_moved(self, event):
        self._process("moved", event.dest_path)

def start_monitor(paths, recursive, detector, alert_manager, response_manager):
    observer = Observer()
    handler = RansomwareEventHandler(detector, alert_manager, response_manager)

    for raw_path in paths:
        path = Path(raw_path)
        path.mkdir(parents=True, exist_ok=True)
        observer.schedule(handler, str(path), recursive=bool(recursive))

    observer.start()
    return observer

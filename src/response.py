from pathlib import Path
import shutil
import hashlib
import time

class ResponseManager:
    def __init__(self, config):
        self.cfg = config["response"]

    def handle(self, alert):
        if not self.cfg.get("enabled", True):
            return

        # Conservative educational response: logging is always safe.
        if not self.cfg.get("quarantine_enabled", False):
            return

        quarantine = Path(self.cfg["quarantine_dir"])
        quarantine.mkdir(parents=True, exist_ok=True)

        # Only process paths included in this detector alert.
        for raw_path in alert.get("sample_paths", []):
            source = Path(raw_path)
            if not source.is_file():
                continue

            digest = hashlib.sha256(
                (str(source) + str(time.time_ns())).encode()
            ).hexdigest()[:12]

            destination = quarantine / f"{digest}_{source.name}"
            try:
                shutil.move(str(source), str(destination))
            except (OSError, PermissionError):
                # Response must never crash the monitoring service.
                continue

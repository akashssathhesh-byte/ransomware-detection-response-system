import json
import logging
from pathlib import Path

class AlertManager:
    def __init__(self, alert_file, application_log):
        self.alert_file = Path(alert_file)
        self.application_log = Path(application_log)

        self.alert_file.parent.mkdir(parents=True, exist_ok=True)
        self.application_log.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=self.application_log,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s"
        )

    def emit(self, alert):
        with self.alert_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(alert) + "\n")

        logging.warning("Security alert: %s", json.dumps(alert))
        print("\n[!] RANSOMWARE-LIKE ACTIVITY DETECTED")
        print(f"    Risk score : {alert['risk_score']}/100")
        print(f"    Reasons    : {', '.join(alert['reasons'])}")
        print(f"    Events     : {alert['recent_event_count']}")

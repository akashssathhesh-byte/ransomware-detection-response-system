import logging
import time

from .alerts import AlertManager
from .config import load_config
from .detector import DetectionEngine
from .monitor import start_monitor
from .response import ResponseManager

def main():
    config = load_config()

    alert_manager = AlertManager(
        config["logging"]["alert_file"],
        config["logging"]["application_log"],
    )
    detector = DetectionEngine(config)
    response_manager = ResponseManager(config)

    observer = start_monitor(
        config["monitor"]["paths"],
        config["monitor"]["recursive"],
        detector,
        alert_manager,
        response_manager,
    )

    print("Ransomware Detection & Response System")
    print("Monitoring:", ", ".join(config["monitor"]["paths"]))
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitor...")
    finally:
        observer.stop()
        observer.join()
        logging.info("Monitoring stopped.")

if __name__ == "__main__":
    main()

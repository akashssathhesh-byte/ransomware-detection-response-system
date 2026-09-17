from pathlib import Path
import yaml

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    monitor = cfg.setdefault("monitor", {})
    detection = cfg.setdefault("detection", {})
    response = cfg.setdefault("response", {})
    logging = cfg.setdefault("logging", {})

    monitor.setdefault("paths", ["./data"])
    monitor.setdefault("recursive", True)

    detection.setdefault("window_seconds", 10)
    detection.setdefault("modification_threshold", 20)
    detection.setdefault("rename_threshold", 10)
    detection.setdefault("suspicious_extension_threshold", 5)
    detection.setdefault("entropy_threshold", 7.2)
    detection.setdefault("risk_threshold", 60)

    response.setdefault("enabled", True)
    response.setdefault("quarantine_enabled", False)
    response.setdefault("quarantine_dir", "./quarantine")

    logging.setdefault("alert_file", "./logs/alerts.jsonl")
    logging.setdefault("application_log", "./logs/application.log")

    return cfg

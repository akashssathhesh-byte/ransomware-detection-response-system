import tempfile
from pathlib import Path

from src.detector import DetectionEngine

def test_detector_initially_returns_no_alert():
    config = {
        "detection": {
            "window_seconds": 10,
            "modification_threshold": 20,
            "rename_threshold": 10,
            "suspicious_extension_threshold": 5,
            "entropy_threshold": 7.2,
            "risk_threshold": 60,
        }
    }

    detector = DetectionEngine(config)
    assert detector.record("modified", "example.txt") is None

def test_suspicious_extension_can_trigger_detection():
    config = {
        "detection": {
            "window_seconds": 10,
            "modification_threshold": 100,
            "rename_threshold": 100,
            "suspicious_extension_threshold": 2,
            "entropy_threshold": 99,
            "risk_threshold": 20,
        }
    }

    detector = DetectionEngine(config)
    detector.record("created", "one.locked")
    alert = detector.record("created", "two.locked")

    assert alert is not None
    assert alert["event"] == "RANSOMWARE_LIKE_ACTIVITY"

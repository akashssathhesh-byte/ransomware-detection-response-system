from collections import deque
from datetime import datetime, timezone
from pathlib import Path
import threading

from .utils import calculate_entropy, is_suspicious_extension, is_suspicious_name

class DetectionEngine:
    def __init__(self, config):
        self.cfg = config["detection"]
        self.window = float(self.cfg["window_seconds"])
        self.events = deque()
        self.lock = threading.Lock()

    def record(self, event_type, path):
        now = datetime.now(timezone.utc).timestamp()

        with self.lock:
            self.events.append((now, event_type, str(path)))
            cutoff = now - self.window
            while self.events and self.events[0][0] < cutoff:
                self.events.popleft()

            return self._evaluate(now)

    def _evaluate(self, now):
        recent = list(self.events)

        modifications = sum(e[1] == "modified" for e in recent)
        renames = sum(e[1] == "moved" for e in recent)
        suspicious = sum(
            e[1] in {"created", "modified", "moved"} and
            (is_suspicious_extension(e[2]) or is_suspicious_name(e[2]))
            for e in recent
        )

        score = 0
        reasons = []

        if modifications >= int(self.cfg["modification_threshold"]):
            score += 25
            reasons.append("rapid file modification activity")

        if renames >= int(self.cfg["rename_threshold"]):
            score += 20
            reasons.append("rapid file rename activity")

        if suspicious >= int(self.cfg["suspicious_extension_threshold"]):
            score += 25
            reasons.append("burst of suspicious file extensions or names")

        # Entropy is checked only on the most recent modified/created file.
        candidate = None
        for _, event_type, path in reversed(recent):
            if event_type in {"modified", "created"}:
                candidate = path
                break

        entropy = calculate_entropy(candidate) if candidate else None
        if entropy is not None and entropy >= float(self.cfg["entropy_threshold"]):
            score += 15
            reasons.append(f"high file entropy ({entropy:.2f})")

        for _, _, path in reversed(recent):
            if is_suspicious_name(path):
                score += 15
                reasons.append("suspicious ransomware-style filename")
                break

        score = min(score, 100)

        if score < int(self.cfg["risk_threshold"]):
            return None

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": "HIGH",
            "risk_score": score,
            "event": "RANSOMWARE_LIKE_ACTIVITY",
            "reasons": sorted(set(reasons)),
            "recent_event_count": len(recent),
            "sample_paths": [e[2] for e in recent[-10:]],
        }

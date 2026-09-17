# Ransomware Detection & Response System

A defensive cybersecurity internship project that monitors file-system activity, detects ransomware-like behavior, generates alerts, and performs configurable response actions.

## Project goals

- Monitor selected directories in real time
- Detect suspicious mass file modifications/renames
- Detect rapid creation of files with suspicious extensions
- Calculate file entropy as a supporting signal
- Use configurable thresholds from `config.yaml`
- Generate structured JSON/JSONL security alerts
- Optionally quarantine suspicious files
- Provide a simple incident summary
- Keep the project safe: it detects behavior and does **not** contain ransomware or file-encryption code

## Architecture

```text
                    +----------------------+
                    |   File System        |
                    | monitored directories |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   File Monitor       |
                    |      watchdog        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Detection Engine      |
                    | - burst activity      |
                    | - extension changes  |
                    | - entropy signal     |
                    | - suspicious names   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Risk Scoring Engine  |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +----------------+          +----------------+
        | Alert Manager  |          | Response       |
        | JSON/JSONL     |          | quarantine/log |
        +----------------+          +----------------+
```

## Folder structure

```text
ransomware-detection-response-system/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── detector.py
│   ├── monitor.py
│   ├── response.py
│   ├── alerts.py
│   └── utils.py
├── tests/
│   └── test_detector.py
├── data/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
├── quarantine/
│   └── .gitkeep
├── config.yaml
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Installation

Python 3.10+ is recommended.

```bash
git clone https://github.com/YOUR-USERNAME/ransomware-detection-response-system.git
cd ransomware-detection-response-system

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
```

## Configuration

Edit `config.yaml`.

By default, the project monitors the local `data/` directory so it can be tested safely.

```yaml
monitor:
  paths:
    - "./data"
  recursive: true

detection:
  window_seconds: 10
  modification_threshold: 20
  rename_threshold: 10
  suspicious_extension_threshold: 5
  entropy_threshold: 7.2
  risk_threshold: 60

response:
  enabled: true
  quarantine_enabled: false
  quarantine_dir: "./quarantine"

logging:
  alert_file: "./logs/alerts.jsonl"
  application_log: "./logs/application.log"
```

## Run

```bash
python -m src.main
```

The program will monitor the configured directory and write alerts to:

```text
logs/alerts.jsonl
```

## Safe testing

Do **not** use real ransomware or intentionally encrypt personal files.

Instead, create harmless test activity inside `data/`:

```bash
mkdir -p data/test
for i in $(seq 1 30); do echo "test-$i" > data/test/file_$i.txt; done
```

Then modify or rename several test files. The detector should observe the activity and may generate a high-risk alert depending on the configured thresholds.

## Detection logic

The prototype uses multiple behavioral indicators rather than treating a single event as proof of ransomware:

| Signal | Example | Weight |
|---|---|---:|
| Rapid modifications | Many writes in a short window | 25 |
| Rapid renames | Multiple renames in a short window | 20 |
| Suspicious extensions | Burst of uncommon extensions | 25 |
| High entropy | File content has unusually high entropy | 15 |
| Suspicious filename | Known ransomware-style suffix pattern | 15 |

The final score is capped at 100.

A score at or above `risk_threshold` creates a high-risk alert.

## Response

The response layer is intentionally conservative.

- Always log the alert.
- Print an incident summary.
- Quarantine is **disabled by default**.
- If enabled, only files explicitly identified by the detector can be moved to the configured quarantine directory.
- The project does not delete files or decrypt files.

## Example alert

```json
{
  "timestamp": "2026-09-17T10:30:00+05:30",
  "severity": "HIGH",
  "risk_score": 75,
  "event": "RANSOMWARE_LIKE_ACTIVITY",
  "reasons": [
    "rapid file modification activity",
    "rapid file rename activity"
  ]
}
```
## Internship deliverables
This repository can support:
1. Project proposal
2. System architecture
3. Functional requirements
4. Threat model
5. Detection-engine implementation
6. Configuration management
7. Alerting and response
8. Unit testing
9. GitHub documentation
10. Final internship presentation/demo

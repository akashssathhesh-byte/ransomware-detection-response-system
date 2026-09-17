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

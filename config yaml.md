monitoring:
  enabled: true
  directories:
    - "./test_folder"

detection:
  file_modification_threshold: 10
  suspicious_extensions:
    - ".locked"
    - ".encrypted"
    - ".crypto"

response:
  generate_alert: true
  quarantine_files: true
  create_report: true

logging:
  level: "INFO"
  file: "logs/system.log"

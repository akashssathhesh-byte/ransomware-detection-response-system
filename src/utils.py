import math
from pathlib import Path

SUSPICIOUS_EXTENSIONS = {
    ".locked", ".encrypted", ".enc", ".crypt", ".crypto",
    ".ransom", ".wncry", ".lockbit", ".akira"
}

SUSPICIOUS_SUFFIXES = (
    ".locked", ".encrypted", ".enc", ".crypt", ".ransom"
)

def calculate_entropy(path, sample_size=1024 * 1024):
    try:
        with open(path, "rb") as f:
            data = f.read(sample_size)
    except (OSError, PermissionError):
        return None

    if not data:
        return 0.0

    counts = [0] * 256
    for byte in data:
        counts[byte] += 1

    length = len(data)
    entropy = 0.0
    for count in counts:
        if count:
            p = count / length
            entropy -= p * math.log2(p)
    return entropy

def is_suspicious_extension(path):
    return Path(path).suffix.lower() in SUSPICIOUS_EXTENSIONS

def is_suspicious_name(path):
    return Path(path).name.lower().endswith(SUSPICIOUS_SUFFIXES)

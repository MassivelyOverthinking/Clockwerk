#-------------------- Imports --------------------

from dataclasses import dataclass
from datetime import datetime

#-------------------- Monitor Configurations --------------------

ENDPOINTS = [
    {"url: http://www.example.com/auth", "timeout: 2", "alert_threshold: 3"}
]

CHECK_INTERVAL = 60         # Measured in seconds
LATENCY_THRESHOLD = 1.5     # Measured in seconds
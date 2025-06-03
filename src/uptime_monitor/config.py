#-------------------- Imports --------------------

import os

from dataclasses import dataclass
from dotenv import load_dotenv


#-------------------- Monitor Configurations --------------------

load_dotenv("/Users/simon/Desktop/Projects/Uptime Monitor/.env")

ENDPOINTS = [
    {"url: http://www.example.com/auth", "timeout: 2", "alert_threshold: 3"}
]

CHECK_INTERVAL = 60         # Measured in seconds
LATENCY_THRESHOLD = 1.5     # Measured in seconds

#-------------------- E-mail Sender Configurations --------------------

SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_PORT = int(os.getenv("SMTP_PORT", "25"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "root@localhost")
EMAIL_TO = os.getenv("EMAIL_TO", "somebody@example.com")
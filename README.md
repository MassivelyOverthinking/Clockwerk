# 🖥️ Utime Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI - Coming Soon](https://img.shields.io/badge/PyPI-coming--soon-yellow)](https://pypi.org/)

---

Uptime monitor is a Python application designed to monitor the availability and performance 
(latency or status) of various API Endpoints (URLs). It tracks the health of the monitored endpoint and stores the results in a database for future analysis and reporting. The application uses SQLalchemy's ORM-based database interaction to store results, and Asyncio's async sessions for asynchronous operations.

## 🚀 Key Features
* 👀 Monitors multiple endpoints
* 🔁 Tracks endpoint health and status with real-time status updates
* 📕 Logs the latency and status code for each request
* 🫙 Stores monitoring results in a database of your own choice
* ➡️ Supports asynchronous database operations to ensure high performance
* 🚨 Sends alert message to report endpoitn failure or latency
* 🤖 Supports MySQL, Prostgresql and SQLite

## 📦 Installation
```python

pip install async_uptime_monitor 
poetry add async_uptime_monitor

```

## 🌎 Code Usage
>> Start by creating the necessary config models `MonitorConfig`, `EmailConfig`, `DatabaseConfig`.

```python
# Import the necessary config-models and schduling loop
from async_uptime_monitor.scheduler import schduling_loop
from async_uptime_monitor.config import MonitorConfig, EmailConfig, DatabaseConfig
from async_uptime_monitor.models import Endpoint

# Create an instance of the MonitorConfig to specify monitored endpoints.
monitor_config = MonitorConfig(
    endpoints = [
        Endpoint(url: "https://test-exmaple.com", timeout=2, alert_threshold=3),
        Endpoint(url: "https://api_testpoint.org", timeout=3, alert_threshold=2)
    ], 
    check_interval = 60,        # Checks the specified endpoints every 60 seconds.
    latency_threshold = 1.5     # Raises an alert if the endpoint latency exceeds the specified number (seconds)
)

# Model for e-mail configuration used to raise and send alert messages.
email_config = EmailConfig(
    smtp_host="smtp.mailtrap.io",
    smtp_port=587,
    email_from="randommail@yourdomain.com",
    email_to="alerts@yourdomain.com"
)

# Database configuration model (MySQL, Postgresql, SQLite)
db_config = DatabaseConfig(
    db_activation=True,             # Writes results to DB if True.
    db_driver="sqlite",             # Specify the desired DB platform.
    db_name="uptime_monitor.db",    # Identifying name for DB.
    db_user="root",                 # Identifying user for DB.
    db_password="SuperSecret123",   # Individual password for DB access.
    db_host="localhost",            # Host associated with current DB.
    db_port=1200                    # Available port to run DB connection on.
)

```

>> Utilise the config models to create an instance of `scheduling_loop` to run.
>> As Uptime Monitor is an async function it can be run with either `asyncio.run()` or `await`.

```python
# Import the necessary config-models and schduling loop
import asyncio
from async_uptime_monitor.scheduler import schduling_loop
from async_uptime_monitor.config import MonitorConfig, EmailConfig, DatabaseConfig
from async_uptime_monitor.models import Endpoint

# Run the scheduling loop (if running the loop from a synchronous context)
asyncio.run(scheduling_loop(
    monitor_config=monitor_config,
    email_config=email_config,
    db_config=db_config
))

# Run the scheduling loop (if running the loop from an asynchronous context)
await scheduling_loop(
    monitor_config=monitor_config,
    email_config=email_config,
    db_config=db_config
)

```


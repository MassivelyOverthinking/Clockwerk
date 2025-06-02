#-------------------- Imports --------------------

import asyncio
import aiohttp
import aiosmtplib
import json

from models import MonitorResult
from config import LATENCY_THRESHOLD
from utils import create_msg
from email.message import EmailMessage

#-------------------- Reporting Function --------------------

async def handle_result(result: MonitorResult):
    if not result.success:
        alert_subject = f"[OUTAGE ALERT] - {result.endpoint_name} is experiencing an outage"
        alert_msg = create_msg(result=result)
        await send_email_alert(message=alert_msg, subject=alert_subject)
    elif result.latency > LATENCY_THRESHOLD:
        alert_subject = f"[LATENCY ALERT] - {result.endpoint_name} is experiencing latency"
        alert_msg = create_msg(result=result)
        await send_email_alert(
            message=json.dumps(alert_msg, indent=2, sort_keys=True, ensure_ascii=True),
            subject=alert_subject
        )

async def send_email_alert(message: str, subject: str):
    email_msg = EmailMessage()
    email_msg["From"] = "root@localhost"
    email_msg["To"] = "somebody@example.com"
    email_msg["Subject"] = subject
    email_msg.set_content(message)
    
    try:
        await aiosmtplib.send(message)
    except aiosmtplib.SMTPException as err:
        print(f"Failed to send the email: {err}")


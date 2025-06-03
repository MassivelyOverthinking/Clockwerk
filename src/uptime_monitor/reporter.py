#-------------------- Imports --------------------

import asyncio
import aiohttp
import aiosmtplib

from models import MonitorResult
from config import LATENCY_THRESHOLD
from utils import create_msg
from models import EmailConfig
from email.message import EmailMessage

#-------------------- Reporting Function --------------------

async def handle_result(result: MonitorResult):
    if not result.success:
        alert_subject = f"[OUTAGE ALERT] - {result.endpoint_name} is experiencing an outage"
        alert_msg = create_msg(result=result)
        await send_email_alert(
            message=alert_msg,
            subject=alert_subject
        )
    elif result.latency >= LATENCY_THRESHOLD:
        alert_subject = f"[LATENCY ALERT] - {result.endpoint_name} is experiencing latency"
        alert_msg = create_msg(result=result)
        await send_email_alert(
            message=alert_msg,
            subject=alert_subject
        )

async def send_email_alert(message: str, subject: str, config: EmailConfig):
    email_msg = EmailMessage()
    email_msg["From"] = config.email_from
    email_msg["To"] = config.email_to
    email_msg["Subject"] = subject
    email_msg.set_content(message)
    
    try:
        await aiosmtplib.send(
            email_msg, hostname=config.smtp_host, port=config.smtp_port
        )
    except aiosmtplib.SMTPException as err:
        print(f"Failed to send the email: {err}")


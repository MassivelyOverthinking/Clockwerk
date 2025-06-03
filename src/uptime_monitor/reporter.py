#-------------------- Imports --------------------

import asyncio
import aiohttp
import aiosmtplib

from utils import create_msg
from models import EmailConfig, MonitorConfig, LoggerConfig, MonitorResult
from email.message import EmailMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from logger import setup_logger

#-------------------- Logger Setup --------------------

log_config = LoggerConfig(
    log_level="INFO",
    log_file="monitor.log",
    log_to_file=True
)

logger = setup_logger(__name__, log_config)

#-------------------- Reporting Function --------------------

async def handle_result(result: MonitorResult, monitor_config: MonitorConfig, email_config: EmailConfig):
    if not result.success:
        alert_subject = f"[OUTAGE ALERT] - {result.endpoint_name} is experiencing an outage"
        alert_msg = create_msg(result=result)
        await send_email_alert(
            message=alert_msg,
            subject=alert_subject
        )
    elif result.latency >= monitor_config.latency_threshold:
        alert_subject = f"[LATENCY ALERT] - {result.endpoint_name} is experiencing latency"
        alert_msg = create_msg(result=result)
        await send_email_alert(
            message=alert_msg,
            subject=alert_subject,
            config=email_config
        )

@retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(aiosmtplib.SMTPException)
)
async def send_email_alert(message: str, subject: str, email_config: EmailConfig):
    email_msg = EmailMessage()
    email_msg["From"] = email_config.email_from
    email_msg["To"] = email_config.email_to
    email_msg["Subject"] = subject
    email_msg.set_content(message)
    
    try:
        await aiosmtplib.send(
            email_msg, hostname=email_config.smtp_host, port=email_config.smtp_port
        )
    except aiosmtplib.SMTPException as err:
        logger.info(f"Failed to send the email: {err}")


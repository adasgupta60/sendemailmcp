import os
import re
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

from fastmcp import FastMCP


mcp = FastMCP("gmail-sender")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(email: str) -> str:
    trimmed = email.strip()
    if not EMAIL_PATTERN.match(trimmed):
        raise ValueError("Invalid recipient email address format.")
    return trimmed


def _read_config() -> tuple[str, str, str, int]:
    sender = os.getenv("GMAIL_ADDRESS", "").strip()
    # Google shows app passwords in 4x4 groups; SMTP expects the same value without spaces.
    app_password = "".join(os.getenv("GMAIL_APP_PASSWORD", "").split())
    smtp_host = os.getenv("GMAIL_SMTP_HOST", "smtp.gmail.com").strip()
    smtp_port_raw = os.getenv("GMAIL_SMTP_PORT", "587").strip()

    if not sender:
        raise RuntimeError("Missing GMAIL_ADDRESS environment variable.")
    if not app_password:
        raise RuntimeError("Missing GMAIL_APP_PASSWORD environment variable.")
    if not EMAIL_PATTERN.match(sender):
        raise RuntimeError("GMAIL_ADDRESS must be a valid email address.")

    try:
        smtp_port = int(smtp_port_raw)
    except ValueError as exc:
        raise RuntimeError("GMAIL_SMTP_PORT must be an integer.") from exc

    return sender, app_password, smtp_host, smtp_port


@mcp.tool(
    name="send_gmail",
    description=(
        "Send an email via Gmail SMTP. "
        "Inputs: recipient_email (string), body (string), optional subject (string)."
    ),
)
def send_gmail(recipient_email: str, body: str, subject: str = "Message from MCP server") -> str:
    recipient = _validate_email(recipient_email)
    if not body or not body.strip():
        raise ValueError("Email body cannot be empty.")

    sender, app_password, smtp_host, smtp_port = _read_config()

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject.strip() if subject.strip() else "Message from MCP server"
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, app_password)
        smtp.send_message(msg)

    sent_at = datetime.now(timezone.utc).isoformat()
    return f"Email sent successfully to {recipient} at {sent_at}"


if __name__ == "__main__":
    # For remote clients, run with:
    # fastmcp run server.py:mcp --transport streamable-http --host 0.0.0.0 --port 8000
    mcp.run()

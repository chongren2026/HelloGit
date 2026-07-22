"""通过可配置的 SMTP 邮箱发送科研检索结果附件。"""

import re
import smtplib
from collections.abc import Callable
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from app.settings import get_settings


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(address: str) -> str:
    normalized = address.strip()
    if not EMAIL_PATTERN.fullmatch(normalized):
        raise ValueError("邮箱地址格式不正确")
    return normalized


def send_excel_via_email(
    recipient: str,
    attachment_path: Path,
    topic: str,
    *,
    sender: str | None = None,
    password: str | None = None,
    smtp_host: str | None = None,
    smtp_port: int | None = None,
    smtp_factory: Callable[..., Any] = smtplib.SMTP_SSL,
) -> None:
    recipient = validate_email(recipient)
    if not attachment_path.is_file():
        raise FileNotFoundError(f"Excel 文件不存在：{attachment_path}")

    settings = get_settings()
    sender = sender or settings.smtp_sender
    password = password or settings.smtp_password
    smtp_host = smtp_host or settings.smtp_host
    smtp_port = smtp_port or settings.smtp_port
    if not sender or not password:
        raise RuntimeError(
            "缺少邮箱配置，请在 .env 中填写 SMTP_SENDER 和 SMTP_PASSWORD"
        )

    sender = validate_email(sender)
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = f"科研文献检索结果：{topic}"
    message.set_content(
        f"您好，\n\n附件为“{topic}”的科研文献检索与分析结果。\n"
        "请在正式研究中继续核验原始文献全文和引用。\n"
    )
    message.add_attachment(
        attachment_path.read_bytes(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=attachment_path.name,
    )

    with smtp_factory(smtp_host, smtp_port, timeout=30) as smtp:
        smtp.login(sender, password.replace(" ", ""))
        smtp.send_message(message)

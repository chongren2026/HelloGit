from pathlib import Path

import pytest

from app.capabilities.mailer import send_excel_via_email, validate_email


class FakeSMTP:
    last_instance = None

    def __init__(self, host: str, port: int, timeout: int) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.login_args = None
        self.message = None
        FakeSMTP.last_instance = self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def login(self, sender: str, password: str) -> None:
        self.login_args = (sender, password)

    def send_message(self, message) -> None:
        self.message = message


def test_validate_email_rejects_invalid_address() -> None:
    with pytest.raises(ValueError):
        validate_email("not-an-email")


def test_send_excel_via_email_builds_attachment(tmp_path: Path) -> None:
    attachment = tmp_path / "result.xlsx"
    attachment.write_bytes(b"xlsx-content")

    send_excel_via_email(
        "receiver@example.com",
        attachment,
        "测试主题",
        sender="sender@126.com",
        password="abcd efgh ijkl mnop",
        smtp_host="smtp.126.com",
        smtp_port=465,
        smtp_factory=FakeSMTP,
    )

    smtp = FakeSMTP.last_instance
    assert smtp.host == "smtp.126.com"
    assert smtp.port == 465
    assert smtp.login_args == ("sender@126.com", "abcdefghijklmnop")
    assert smtp.message["To"] == "receiver@example.com"
    assert len(list(smtp.message.iter_attachments())) == 1

"""环境变量和本地路径配置。"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


@dataclass(frozen=True)
class Settings:
    output_dir: Path = OUTPUT_DIR
    openalex_api_key: str | None = None
    smtp_host: str = "smtp.126.com"
    smtp_port: int = 465
    smtp_sender: str | None = None
    smtp_password: str | None = None


def get_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")
    OUTPUT_DIR.mkdir(exist_ok=True)
    return Settings(
        openalex_api_key=os.getenv("OPENALEX_API_KEY"),
        smtp_host=os.getenv("SMTP_HOST", "smtp.126.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "465")),
        smtp_sender=os.getenv("SMTP_SENDER"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
    )

"""环境变量和本地路径配置。"""

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


@dataclass(frozen=True)
class Settings:
    output_dir: Path = OUTPUT_DIR


def get_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")
    OUTPUT_DIR.mkdir(exist_ok=True)
    return Settings()

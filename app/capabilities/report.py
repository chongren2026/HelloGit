"""报告输出能力；第一版生成 Markdown，后续可加入 DOCX。"""

import re
from pathlib import Path

from app.settings import get_settings


def write_markdown_report(topic: str, content: str) -> Path:
    safe_name = re.sub(r"[^\w\-]+", "_", topic, flags=re.UNICODE).strip("_") or "research_report"
    path = get_settings().output_dir / f"{safe_name}.md"
    path.write_text(content, encoding="utf-8")
    return path

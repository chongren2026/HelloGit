"""离线样例数据源，用于在无 API 密钥时验证工作流。"""

from app.models import Paper
from app.providers.base import LiteratureProvider


class MockLiteratureProvider(LiteratureProvider):
    def search(self, topic: str) -> list[Paper]:
        return [
            Paper(
                title=f"{topic}的研究进展",
                authors=["示例作者甲", "示例作者乙"],
                year=2025,
                abstract="本文使用样例数据说明如何从文献题录构建可追溯的初步综述。",
                source_url="https://example.org/sample-paper-1",
            ),
            Paper(
                title=f"{topic}的方法与挑战",
                authors=["示例作者丙"],
                year=2024,
                abstract="本文梳理该主题的常见研究方法、潜在局限与后续研究方向。",
                source_url="https://example.org/sample-paper-2",
            ),
        ]

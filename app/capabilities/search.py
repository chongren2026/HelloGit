"""检索能力：对外只返回统一的 Paper 数据结构。"""

from app.models import Paper
from app.providers.base import LiteratureProvider
from app.providers.openalex import OpenAlexProvider


def search_papers(
    topic: str,
    provider: LiteratureProvider | None = None,
) -> list[Paper]:
    active_provider = provider or OpenAlexProvider()
    return active_provider.search(topic)

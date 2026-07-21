"""检索能力：对外只返回统一的 Paper 数据结构。"""

from app.models import Paper
from app.providers.mock import MockLiteratureProvider


def search_papers(topic: str) -> list[Paper]:
    return MockLiteratureProvider().search(topic)

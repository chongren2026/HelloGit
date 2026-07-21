"""OpenAlex 数据源占位。

接入前需实现 LiteratureProvider.search，并记录数据源 URL、查询条件和检索日期。
"""

from app.models import Paper
from app.providers.base import LiteratureProvider


class OpenAlexProvider(LiteratureProvider):
    def search(self, topic: str) -> list[Paper]:
        raise NotImplementedError("OpenAlexProvider 尚未接入；请先使用 MockLiteratureProvider。")

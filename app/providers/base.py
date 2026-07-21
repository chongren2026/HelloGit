"""文献数据源的统一接口。"""

from abc import ABC, abstractmethod

from app.models import Paper


class LiteratureProvider(ABC):
    @abstractmethod
    def search(self, topic: str) -> list[Paper]:
        """根据主题返回规范化文献列表。"""

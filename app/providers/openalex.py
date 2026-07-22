"""OpenAlex 公开文献元数据源与基础相关性筛选。"""

from dataclasses import replace
from typing import Any

import httpx

from app.models import Paper
from app.providers.base import LiteratureProvider
from app.settings import get_settings


SPORTS_CULTURE_DIGITAL_GROUPS: tuple[tuple[str, ...], ...] = (
    ("体育", "运动", "sport", "athletic"),
    ("文化", "culture", "cultural"),
    (
        "数字传播",
        "数字媒介",
        "数字化传播",
        "新媒体",
        "社交媒体",
        "短视频",
        "digital communication",
        "digital dissemination",
        "digital media",
        "new media",
        "social media",
    ),
)


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str:
    """将 OpenAlex 的倒排索引摘要还原为普通文本。"""
    if not index:
        return ""

    positioned_words = [
        (position, word)
        for word, positions in index.items()
        for position in positions
    ]
    positioned_words.sort(key=lambda item: item[0])
    return " ".join(word for _, word in positioned_words)


def _authors_from_work(work: dict[str, Any]) -> list[str]:
    authors = []
    for authorship in work.get("authorships", []):
        name = authorship.get("author", {}).get("display_name")
        if name:
            authors.append(name)
    return authors


def build_search_query(topic: str) -> str:
    """为已知研究主题构造更严格的布尔检索式。"""
    compact_topic = "".join(topic.split())
    if all(term in compact_topic for term in ("体育", "文化", "数字", "传播")):
        return (
            '(体育 AND 文化) AND ("数字传播" OR "数字媒介" '
            'OR "数字化传播" OR "新媒体" OR "digital media" '
            'OR "digital communication")'
        )
    return topic


def relevance_groups_for_topic(topic: str) -> tuple[tuple[str, ...], ...]:
    """返回必须同时命中的概念组；普通主题暂不强制本地过滤。"""
    compact_topic = "".join(topic.split())
    if all(term in compact_topic for term in ("体育", "文化", "数字", "传播")):
        return SPORTS_CULTURE_DIGITAL_GROUPS
    return ()


def _matches_for_group(text: str, group: tuple[str, ...]) -> list[str]:
    lowered_text = text.lower()
    return [term for term in group if term.lower() in lowered_text]


def filter_relevant_papers(
    topic: str,
    candidates: list[Paper],
    limit: int = 5,
) -> list[Paper]:
    """要求每个主题概念组至少命中一个词，再按标题覆盖与 OpenAlex 分数排序。"""
    groups = relevance_groups_for_topic(topic)
    if not groups:
        return [
            replace(
                paper,
                inclusion_reason="按 OpenAlex 文本相关性排序纳入；尚未配置专项关键词组。",
            )
            for paper in candidates[:limit]
        ]

    ranked: list[tuple[int, float, Paper]] = []
    for paper in candidates:
        full_text = f"{paper.title}\n{paper.abstract}"
        matches_by_group = [_matches_for_group(full_text, group) for group in groups]
        if not all(matches_by_group):
            continue

        title_group_hits = sum(
            bool(_matches_for_group(paper.title, group)) for group in groups
        )
        matched_terms = tuple(
            dict.fromkeys(term for matches in matches_by_group for term in matches)
        )
        score = paper.openalex_relevance_score or 0.0
        included = replace(
            paper,
            matched_terms=matched_terms,
            inclusion_reason=(
                "标题或摘要同时覆盖体育、文化和数字传播三个概念组；"
                f"其中 {title_group_hits} 个概念组在标题中命中。"
            ),
        )
        ranked.append((title_group_hits, score, included))

    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [paper for _, _, paper in ranked[:limit]]


class OpenAlexProvider(LiteratureProvider):
    BASE_URL = "https://api.openalex.org/works"

    def __init__(
        self,
        per_page: int = 30,
        max_results: int = 5,
        timeout_seconds: float = 20.0,
    ) -> None:
        if not 1 <= per_page <= 100:
            raise ValueError("per_page 必须在 1 到 100 之间")
        if not 1 <= max_results <= per_page:
            raise ValueError("max_results 必须在 1 到 per_page 之间")
        self.per_page = per_page
        self.max_results = max_results
        self.timeout_seconds = timeout_seconds

    def search(self, topic: str) -> list[Paper]:
        api_key = get_settings().openalex_api_key
        if not api_key:
            raise RuntimeError("缺少 OPENALEX_API_KEY，请在项目根目录的 .env 中配置")

        try:
            # OpenAlex 偶尔会出现短暂的 DNS/连接失败；仅对建立连接阶段自动重试。
            transport = httpx.HTTPTransport(retries=2)
            with httpx.Client(
                transport=transport,
                timeout=self.timeout_seconds,
                follow_redirects=True,
                headers={"User-Agent": "AI-Research-Assistant/0.1"},
            ) as client:
                response = client.get(
                    self.BASE_URL,
                params={
                    "api_key": api_key,
                    "search": build_search_query(topic),
                    "per_page": self.per_page,
                    "sort": "relevance_score:desc",
                    "select": (
                        "id,doi,title,publication_year,authorships,"
                        "abstract_inverted_index,relevance_score"
                    ),
                },
                )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"OpenAlex API 返回错误状态 {exc.response.status_code}"
            ) from None
        except httpx.RequestError as exc:
            raise RuntimeError(
                "无法连接 OpenAlex API。请确认浏览器服务由 PyCharm Terminal 启动，"
                f"并检查网络或代理设置。技术原因：{type(exc).__name__}"
            ) from None

        papers = []
        for work in response.json().get("results", []):
            papers.append(
                Paper(
                    title=work.get("title") or "无标题",
                    authors=_authors_from_work(work) or ["作者未知"],
                    year=work.get("publication_year") or 0,
                    abstract=(
                        reconstruct_abstract(work.get("abstract_inverted_index"))
                        or "OpenAlex 未提供摘要"
                    ),
                    source_url=work.get("doi") or work.get("id"),
                    openalex_relevance_score=work.get("relevance_score"),
                )
            )
        return filter_relevant_papers(topic, papers, limit=self.max_results)

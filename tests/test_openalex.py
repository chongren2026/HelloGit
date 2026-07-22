from app.models import Paper
from app.providers.openalex import (
    build_search_query,
    filter_relevant_papers,
    reconstruct_abstract,
)


def test_reconstruct_abstract() -> None:
    index = {"AI": [0], "sports": [1], "training": [2]}
    assert reconstruct_abstract(index) == "AI sports training"


def test_reconstruct_empty_abstract() -> None:
    assert reconstruct_abstract(None) == ""


def test_builds_strict_query_for_sports_culture_digital_topic() -> None:
    query = build_search_query("体育文化数字传播研究")
    assert "体育 AND 文化" in query
    assert "数字传播" in query


def test_filters_partial_matches_and_explains_inclusion() -> None:
    candidates = [
        Paper(
            title="体育文化的数字传播路径",
            authors=["作者甲"],
            year=2025,
            abstract="研究体育文化如何借助数字媒介和新媒体传播。",
            openalex_relevance_score=100.0,
        ),
        Paper(
            title="高校体育数字化教学",
            authors=["作者乙"],
            year=2024,
            abstract="研究体育教学中的数字技术。",
            openalex_relevance_score=200.0,
        ),
        Paper(
            title="区域文化的数字传播",
            authors=["作者丙"],
            year=2024,
            abstract="研究地方文化的新媒体传播。",
            openalex_relevance_score=150.0,
        ),
    ]

    selected = filter_relevant_papers("体育文化数字传播研究", candidates)

    assert len(selected) == 1
    assert selected[0].title == "体育文化的数字传播路径"
    assert "体育" in selected[0].matched_terms
    assert selected[0].inclusion_reason

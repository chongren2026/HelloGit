from app.capabilities.analyze import analyze_paper
from app.models import Paper


def test_analyze_paper_retains_source_paper() -> None:
    paper = Paper("测试论文", ["作者"], 2025, "测试摘要")
    analysis = analyze_paper(paper)
    assert analysis.paper is paper
    assert "测试摘要" in analysis.finding

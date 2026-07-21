from app.capabilities.search import search_papers


def test_search_returns_papers() -> None:
    papers = search_papers("人工智能辅助科研")
    assert len(papers) == 2
    assert papers[0].title

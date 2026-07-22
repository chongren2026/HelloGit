"""科研任务的顺序工作流；后续可替换为 LangGraph。"""

from app.capabilities.analyze import analyze_papers
from app.capabilities.report import write_markdown_report
from app.capabilities.review import create_review
from app.capabilities.search import search_papers
from app.capabilities.spreadsheet import write_excel_report
from app.models import ResearchState
from app.providers.base import LiteratureProvider


def run_research(
    topic: str,
    provider: LiteratureProvider | None = None,
) -> ResearchState:
    state = ResearchState(topic=topic)
    state.papers = search_papers(topic, provider=provider)
    state.analyses = analyze_papers(state.papers)
    state.review_markdown = create_review(topic, state.analyses)
    state.report_path = write_markdown_report(topic, state.review_markdown)
    state.excel_path = write_excel_report(topic, state.analyses)
    return state

"""工作流中的共享数据模型。"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Paper:
    title: str
    authors: list[str]
    year: int
    abstract: str
    source_url: str | None = None


@dataclass(frozen=True)
class Analysis:
    paper: Paper
    background: str
    method: str
    finding: str
    limitations: str


@dataclass
class ResearchState:
    topic: str
    papers: list[Paper] = field(default_factory=list)
    analyses: list[Analysis] = field(default_factory=list)
    review_markdown: str = ""
    report_path: Path | None = None

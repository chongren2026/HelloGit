"""单篇论文的最小结构化分析能力。"""

from app.models import Analysis, Paper


def analyze_paper(paper: Paper) -> Analysis:
    return Analysis(
        paper=paper,
        background=f"围绕“{paper.title}”讨论的研究问题。",
        method="当前为样例规则分析；后续可接入 LLM 或 PDF 全文提取。",
        finding=paper.abstract,
        limitations="仅基于题录与摘要，尚未核验全文证据。",
    )


def analyze_papers(papers: list[Paper]) -> list[Analysis]:
    return [analyze_paper(paper) for paper in papers]

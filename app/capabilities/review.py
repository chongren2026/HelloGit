"""多篇论文分析的综述生成能力。"""

from app.models import Analysis


def create_review(topic: str, analyses: list[Analysis]) -> str:
    lines = [f"# {topic}：初步文献综述", "", "## 纳入文献"]
    for index, analysis in enumerate(analyses, start=1):
        paper = analysis.paper
        lines.extend(
            [
                f"### {index}. {paper.title} ({paper.year})",
                f"- 作者：{', '.join(paper.authors)}",
                f"- 主要发现：{analysis.finding}",
                f"- 局限：{analysis.limitations}",
            ]
        )
        if paper.source_url:
            lines.append(f"- 来源：{paper.source_url}")

    lines.extend(["", "## 初步结论", "本报告由样例数据生成；正式研究前应核验原始文献与引用。"])
    return "\n".join(lines) + "\n"

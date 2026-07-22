"""多篇论文分析的综述生成能力。"""

from app.models import Analysis


def create_review(topic: str, analyses: list[Analysis]) -> str:
    lines = [
        f"# {topic}：初步文献综述",
        "",
        "## 检索与筛选说明",
        "OpenAlex 先返回候选文献，再根据研究主题的必要概念组进行本地筛选。",
        "仅纳入同时满足全部必要概念组的文献；不足目标数量时不使用低相关文献补足。",
        "",
        "## 纳入文献",
    ]
    if not analyses:
        lines.append("未找到同时满足全部必要概念组的文献。建议调整关键词后重新检索。")

    for index, analysis in enumerate(analyses, start=1):
        paper = analysis.paper
        lines.extend(
            [
                f"### {index}. {paper.title} ({paper.year})",
                f"- 作者：{', '.join(paper.authors)}",
                (
                    "- OpenAlex 相关性分数："
                    f"{paper.openalex_relevance_score:.2f}"
                    if paper.openalex_relevance_score is not None
                    else "- OpenAlex 相关性分数：未提供"
                ),
                (
                    f"- 命中关键词：{', '.join(paper.matched_terms)}"
                    if paper.matched_terms
                    else "- 命中关键词：未配置专项关键词组"
                ),
                f"- 纳入理由：{paper.inclusion_reason or '数据源返回的候选文献'}",
                f"- 主要发现：{analysis.finding}",
                f"- 局限：{analysis.limitations}",
            ]
        )
        if paper.source_url:
            lines.append(f"- 来源：{paper.source_url}")

    lines.extend(
        [
            "",
            "## 初步结论",
            "本报告基于 OpenAlex 题录与摘要生成；正式研究前仍应核验原始文献全文与引用。",
        ]
    )
    return "\n".join(lines) + "\n"

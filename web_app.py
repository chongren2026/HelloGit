"""AI 科研助手的本地 Streamlit 网页入口。"""

from pathlib import Path

import streamlit as st

from app.capabilities.mailer import send_excel_via_email, validate_email
from app.models import ResearchState
from app.workflow import run_research


st.set_page_config(
    page_title="AI 科研助手",
    page_icon="🔬",
    layout="wide",
)


def _download_button(label: str, path: Path, mime: str) -> None:
    st.download_button(
        label=label,
        data=path.read_bytes(),
        file_name=path.name,
        mime=mime,
        use_container_width=True,
    )


def _show_result(result: ResearchState) -> None:
    st.success(f"检索完成，共纳入 {len(result.papers)} 篇文献。")

    left, right = st.columns(2)
    if result.report_path and result.report_path.is_file():
        with left:
            _download_button(
                "下载 Markdown 综述",
                result.report_path,
                "text/markdown",
            )
    if result.excel_path and result.excel_path.is_file():
        with right:
            _download_button(
                "下载 Excel 检索结果",
                result.excel_path,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    st.subheader("综述预览")
    st.markdown(result.review_markdown)

    with st.expander("查看纳入文献"):
        for index, paper in enumerate(result.papers, start=1):
            st.markdown(f"**{index}. {paper.title}（{paper.year}）**")
            st.caption(
                f"作者：{', '.join(paper.authors) or '未知'}｜"
                f"相关性分数：{paper.openalex_relevance_score or 0:.2f}"
            )
            if paper.source_url:
                st.link_button("打开文献页面", paper.source_url)


def main() -> None:
    st.title("🔬 AI 科研助手")
    st.write("输入研究主题，自动检索文献、生成初步综述和 Excel 结果。")

    with st.form("research_form"):
        topic = st.text_input(
            "研究主题",
            placeholder="例如：AI 赋能体育产业",
        )
        recipient = st.text_input(
            "接收邮箱（可选）",
            placeholder="填写后会将 Excel 结果发送到该邮箱",
        )
        submitted = st.form_submit_button(
            "开始检索",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        topic = topic.strip()
        recipient = recipient.strip()
        if not topic:
            st.error("请输入研究主题。")
            return

        try:
            if recipient:
                recipient = validate_email(recipient)
            with st.spinner("正在检索并生成报告，请稍候……"):
                result = run_research(topic)
            st.session_state["research_result"] = result
            st.session_state["email_notice"] = None

            if recipient:
                if result.excel_path is None:
                    raise RuntimeError("Excel 文件尚未生成。")
                with st.spinner("正在发送 Excel 附件……"):
                    send_excel_via_email(recipient, result.excel_path, topic)
                result.email_sent_to = recipient
                st.session_state["email_notice"] = f"Excel 已发送至：{recipient}"
        except Exception as exc:  # 网页入口需要将外部服务错误友好地展示给用户
            st.error(f"任务执行失败：{exc}")
            return

    result = st.session_state.get("research_result")
    if result is not None:
        notice = st.session_state.get("email_notice")
        if notice:
            st.info(notice)
        _show_result(result)


if __name__ == "__main__":
    main()

from app.workflow import run_research


def test_workflow_generates_markdown_report() -> None:
    result = run_research("人工智能辅助科研")
    assert result.report_path is not None
    assert result.report_path.exists()
    assert "初步文献综述" in result.report_path.read_text(encoding="utf-8")

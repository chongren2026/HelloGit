# AI Research Assistant

一个从研究主题出发，检索样例文献、生成结构化分析和 Markdown 报告的最小科研助手骨架。

## 当前能力

- 使用固定样例文献跑通检索、分析、综述和报告输出流程。
- 所有输出写入 `outputs/`，不会提交到 Git。
- 尚未接入外部文献 API、PDF 全文处理或大模型。

## 运行

```powershell
cd ai-research-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## 后续扩展

将 `app.providers.mock.MockLiteratureProvider` 替换为公开数据源实现，例如 `OpenAlexProvider`；接入时应保留来源 URL 和检索日期，保证综述内容可追溯。

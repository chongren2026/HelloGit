# AI Research Assistant

一个从研究主题出发，检索真实文献、生成结构化分析、Excel 结果和 Markdown 报告的科研助手 MVP。

## 当前能力

- 使用 OpenAlex 检索真实文献，并执行关键词相关性筛选。
- 生成 Markdown 综述和结构化 Excel 检索结果。
- 输入收件邮箱后，可使用本地配置的 126 邮箱发送 Excel 附件。
- 所有输出写入 `outputs/`，不会提交到 Git。
- 尚未接入 PDF 全文处理；当前“AI总结”使用已有结构化分析结果。

## 运行

```powershell
cd HelloGit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## 网页界面

安装依赖后，在项目目录运行：

```powershell
streamlit run web_app.py
```

浏览器会自动打开本地网页。输入研究主题即可生成综述与 Excel；接收邮箱为可选项，填写后会通过 `.env` 中配置的 126 邮箱发送 Excel 附件。停止网页服务时，在 Terminal 中按 `Ctrl+C`。

## 本地配置

复制 `.env.example` 为 `.env`，并填写：

```env
OPENALEX_API_KEY=你的OpenAlex密钥
SMTP_HOST=smtp.126.com
SMTP_PORT=465
SMTP_SENDER=你的126邮箱地址
SMTP_PASSWORD=126邮箱生成的客户端授权码
```

不要填写邮箱网页登录密码，也不要提交 `.env`。126 邮箱需要先开启 SMTP 服务并生成客户端授权码。

# AI Research Assistant 项目交接

更新日期：2026-07-24
本地目录：`C:\Users\Administrator\Documents\New project for test\HelloGit`
GitHub：<https://github.com/chongren2026/HelloGit>
云端应用：<https://hellogit-bbyfmrb5ywptmqwcu2bpqy.streamlit.app/>

## 1. 项目目标与讨论边界

这是一个简化的中文科研 AI 助手 MVP。当前目标是：

1. 用户输入研究主题。
2. 从合规的公开文献数据源检索真实文献。
3. 对题录和摘要做结构化分析。
4. 生成 Markdown 初步综述和 Excel 检索结果。
5. 用户可下载结果，或通过配置好的 126 邮箱发送 Excel。
6. 同时支持本地命令行、本地网页和 Streamlit Cloud 网页。

本项目只讨论科研 AI 助手，不要混入用户其他会话或其他行业 Agent 项目。

当前没有做知网自动登录、验证码绕过、PDF 批量下载或反爬绕过。后续涉及 CNKI 时必须遵守账号权限、网站条款和版权要求。

## 2. 当前架构

项目没有采用之前讨论过的复杂多 Agent/Skill 平台，也还没有使用 LangGraph。当前是一个容易理解的顺序工作流：

```text
用户输入主题
  → OpenAlex 检索
  → 相关性筛选
  → 摘要结构化分析
  → 生成 Markdown 综述
  → 生成 Excel
  → 可选：126 SMTP 发送附件
```

主要文件：

```text
main.py                         命令行入口
web_app.py                      Streamlit 网页入口

app/models.py                   Paper、Analysis、ResearchState
app/workflow.py                 顺序串联完整工作流
app/settings.py                 从 .env/环境变量读取配置

app/providers/base.py           文献数据源接口
app/providers/mock.py           测试用模拟数据
app/providers/openalex.py       OpenAlex 请求、摘要还原和相关性筛选

app/capabilities/search.py      文献检索能力
app/capabilities/analyze.py     单篇摘要结构化分析
app/capabilities/review.py      多篇文献初步综述
app/capabilities/report.py      Markdown 文件输出
app/capabilities/spreadsheet.py Excel 文件输出
app/capabilities/mailer.py      通用 SMTP SSL 邮件发送

tests/                          自动测试
outputs/                        本地临时结果，不提交 Git
.streamlit/config.toml          Streamlit 普通配置
.env.example                    变量名示例，不含真实秘密
```

## 3. 已完成内容

### 3.1 文献检索

- 已从模拟数据切换到 OpenAlex 真实公开文献元数据。
- OpenAlex API Key 从环境变量 `OPENALEX_API_KEY` 读取。
- 默认拉取最多 30 个候选，最终返回最多 5 篇。
- OpenAlex 的倒排索引摘要会还原成普通文本。
- 请求包含连接重试，降低短暂 DNS/连接错误影响。
- 记录 OpenAlex 相关性分数、命中关键词和纳入理由。
- 对“体育文化数字传播研究”这类主题配置过严格的概念组过滤：
  - 体育
  - 文化
  - 数字传播/数字媒介/新媒体等
- 普通主题目前主要使用 OpenAlex 自身的文本相关性排序，没有为每个领域单独配置概念组。

### 3.2 分析与报告

- 能基于标题和摘要生成结构化 `Analysis`。
- 能生成 Markdown 初步文献综述。
- 能生成 Excel，列名严格为：

```text
序号、作者、相关性分数、命中关键词、纳入理由、摘要内容、AI总结、文档链接
```

- Excel 包含文献链接、适当的列宽、换行和行高。
- 输出写入 `outputs/`。

重要说明：当前“AI总结”还不是真正调用大模型生成，而是由现有结构化规则和摘要分析生成。项目虽然预留了 `OPENAI_API_KEY`、`OPENAI_MODEL`，但尚未接入 OpenAI 或其他 LLM。

### 3.3 邮件

- 已从 Gmail 专用代码改成通用 SMTP 配置。
- 当前使用 126 邮箱：

```text
SMTP_HOST=smtp.126.com
SMTP_PORT=465
SMTP_SENDER=<配置在秘密中>
SMTP_PASSWORD=<126 客户端授权码>
```

- 使用 `SMTP_SSL` 登录并发送 Excel 附件。
- 本地 SMTP 登录测试成功。
- Streamlit Cloud 上“检索 → Excel 下载 → 126 邮件发送”完整闭环也已测试通过。

### 3.4 网页

- 已创建 `web_app.py`。
- 支持输入研究主题。
- 支持可选输入收件邮箱。
- 支持综述预览、纳入文献查看、Markdown 下载和 Excel 下载。
- 本地启动命令：

```powershell
python -m streamlit run web_app.py
```

- 本地网址通常是 `http://localhost:8501`。
- 已部署到 Streamlit Community Cloud。

### 3.5 GitHub 与云端

- 本地远程仓库为：

```text
origin https://github.com/chongren2026/HelloGit.git
```

- 当前使用 `main` 分支。
- 在创建本交接文档前，本地与 `origin/main` 同步，最近提交为：

```text
89f55ff Disable Streamlit onboarding email prompt
c89ab04 Added Dev Container Folder
```

- Streamlit Cloud 已连接 GitHub，推送到 `main` 后会自动重新部署。
- `.env`、`.venv` 和 `outputs/*` 已忽略。
- 云端真实秘密存放在 Streamlit Cloud Secrets，而不是 GitHub。

### 3.6 测试

最近一次结果：

```text
10 passed
```

运行方式：

```powershell
python -m pytest tests -q
```

Pytest 偶尔提示无法创建 `.pytest_cache` 的 `WinError 183`，这是缓存警告，不影响测试通过。

## 4. 当前状态与卡点

当前没有功能性阻塞：

- 本地命令行可用。
- 本地 Streamlit 网页可用。
- 云端 Streamlit 网页可用。
- OpenAlex 检索可用。
- Markdown/Excel 生成可用。
- 126 邮件发送可用。
- 完整云端闭环已由用户验证。

目前真正需要解决的是“公开分享前的安全和产品化”，不是基础功能故障：

1. 需要确认 Streamlit 应用是公开还是私有。
2. 当前网页允许输入任意收件邮箱，会消耗用户的 126 邮箱发送额度；公开链接存在滥用风险。
3. 没有用户登录、每日额度、频率限制或验证码。
4. 输出文件名按主题生成；多人同时搜索相同主题时可能互相覆盖。
5. Streamlit Cloud 文件系统不是永久存储。
6. 当前分析不是真正的大模型总结。

用户已明确要求把本交接文档和 `.gitignore` 更新推送到 GitHub。当前待提交范围只能包含：

```text
.gitignore
HANDOF.md
```

不要使用 `git add .` 扩大提交范围。发布前必须确认 `gh auth status` 成功；2026-07-24 最近一次检查仍提示 GitHub CLI 默认账号令牌无效，因此推送流程停在认证环节。

## 5. 建议的下一阶段计划

### 优先级 P0：分享安全

在把链接广泛分享前完成：

1. 将应用设为仅指定朋友可访问，或增加应用级登录。
2. 限制收件人：
   - 最保守：只允许发送到当前登录用户邮箱。
   - 或设置允许域名/白名单。
3. 增加发送频率限制和每日额度。
4. 搜索和邮件按钮增加防重复提交。
5. 不向网页、日志或错误提示输出任何密钥。

如果只是分享给少数可信朋友，至少先使用 Streamlit Cloud 的 Sharing 权限邀请指定邮箱，不要将公开链接发到群聊、论坛或社交平台。

### 优先级 P1：并发与稳定性

1. 输出文件名增加时间戳或 UUID。
2. 优先使用 `tempfile` 或内存字节流，避免不同用户覆盖同一路径。
3. 为 OpenAlex 增加结果缓存、明确超时和用户友好的错误提示。
4. 对“无结果”和“筛选后 0 篇”单独显示说明。
5. 给邮件发送增加失败重试，但绝对不要无界重试。

### 优先级 P2：检索质量

1. 网页增加：
   - 文献数量
   - 起止年份
   - 语言
   - 开放获取
   - 文献类型
2. 把当前针对单一主题硬编码的概念组改成通用查询策略。
3. 显示完整检索式、候选数量、筛选数量和排除原因。
4. 增加 Crossref、Semantic Scholar 等合规数据源，并做统一去重。
5. 不要把 OpenAlex `relevance_score` 当成论文质量分数；它只表示查询文本相关性。

### 优先级 P3：真正的 AI 分析

1. 接入一个明确的大模型供应商。
2. 使用结构化输出生成：
   - 研究背景
   - 研究问题
   - 方法
   - 主要发现
   - 创新点
   - 局限
3. 明确标注“基于摘要”或“基于全文”，不能把摘要分析伪装成全文结论。
4. 增加引用追溯，任何综合结论都能回到原始文献。
5. 控制 Token 成本、并发量和失败重试。

### 优先级 P4：PDF 与全文

1. 支持用户主动上传合法持有的 PDF。
2. 解析全文并分段。
3. 生成带证据片段和页码的分析。
4. 再考虑 RAG/向量库；现在不要为了“看起来像 Agent”过早引入复杂框架。

## 6. 日常开发与发布流程

每次开始：

```powershell
git pull --rebase origin main
```

修改后：

```powershell
python -m pytest tests -q
python -m streamlit run web_app.py
git status
```

提交时显式选择文件，避免误提交秘密：

```powershell
git add <明确的文件路径>
git commit -m "简洁且具体的修改说明"
git pull --rebase origin main
git push origin main
```

Streamlit Cloud 会根据 GitHub `main` 自动重新部署。

## 7. 配置与秘密

本地 `.env` 应包含的有效变量：

```text
OPENALEX_API_KEY
SMTP_HOST
SMTP_PORT
SMTP_SENDER
SMTP_PASSWORD
```

`GMAIL_SENDER` 和 `GMAIL_APP_PASSWORD` 是旧配置，代码已经不再使用；如果本地 `.env` 仍有这两项，可以删除。

绝对禁止提交：

```text
.env
.streamlit/secrets.toml
真实 API Key
126 邮箱授权码
任何验证码或登录密码
```

当前 `.gitignore` 已显式加入以下规则：

```gitignore
node_modules/
.streamlit/secrets.toml
```

其中 `node_modules/` 是可重建的 Node.js 本地依赖，不能上传；`.streamlit/secrets.toml` 可能保存云端密钥，也绝对不能上传。提交前执行：

```powershell
git status
git check-ignore -v .env .streamlit/secrets.toml
```

用户曾在历史聊天中直接发送过 OpenAlex API Key。不要在新会话中重复显示该值；从安全角度建议用户到 OpenAlex 轮换/重新生成 Key，然后同步更新本地 `.env` 和 Streamlit Cloud Secrets。

## 8. 已踩过的坑——不要再踩

### 8.1 不要提交秘密

- 不要把 `.env`、授权码、API Key 写入代码、README、测试或 GitHub。
- 不要让用户把密钥粘贴到聊天里。
- 示例文件只能保留变量名和无敏感性的默认值。

### 8.2 不要把 Streamlit 普通配置和 Secrets 混淆

- `.streamlit/config.toml` 可以提交。
- `.streamlit/secrets.toml` 不可以提交。
- Streamlit Cloud Secrets 在云端控制台配置。

### 8.3 不要恢复 Streamlit 首次邮箱询问

云端曾因首次启动欢迎提示停在：

```text
Welcome to Streamlit!
Email:
```

随后健康检查报：

```text
connect: connection refused
```

修复依赖 `.streamlit/config.toml`：

```toml
[browser]
gatherUsageStats = false

[server]
headless = false
showEmailPrompt = false
```

不要删除 `showEmailPrompt = false`。

### 8.4 不要同时启动多个本地 Streamlit 服务

之前 8501 端口被两个 Python/Streamlit 进程同时占用，浏览器进入了没有外网权限的旧测试服务，导致明明 OpenAlex 正常却一直显示“无法连接 OpenAlex API”。

排查命令：

```powershell
netstat -ano | findstr ":8501"
```

修改代码后要停止旧服务并重新启动；不要只刷新浏览器。

### 8.5 不要使用 `git push --force` 解决普通 push 冲突

曾出现：

```text
rejected (fetch first)
```

原因是 GitHub 远程增加了 Dev Container 提交。本项目使用：

```powershell
git pull --rebase origin main
git push origin main
```

成功保留双方修改。不要用强制推送覆盖远程内容。

### 8.6 LF/CRLF 警告不是失败

Windows 上：

```text
LF will be replaced by CRLF
```

只是换行符提示，不代表 `git add`、提交或推送失败。

### 8.7 不要把虚拟环境上传

`.venv/` 不应提交。PyCharm 的 `.idea/` 也已忽略。虚拟环境只属于本机，云端依赖由 `requirements.txt` 重建。

### 8.8 不要过早做复杂 Agent 架构

此前设计过多层 `agents/skills/workflows/core`，对当前 MVP 过度复杂。现阶段顺序工作流更清楚。只有当出现真正的条件分支、人工审批、失败恢复或多轮状态时，才考虑 LangGraph。

### 8.9 不要声称当前结果是“全文 AI 阅读”

当前主要证据来自 OpenAlex 题录和摘要：

- 不代表已经阅读 PDF 全文。
- 不保证摘要一定存在。
- AI 总结目前是规则化分析。
- 正式科研结论必须核验原文、作者、期刊、DOI 和引用。

### 8.10 不要假设云端文件永久存在

`outputs/` 适合即时下载和发送，不适合长期保存。多人使用前必须解决并发文件名和临时存储问题。

### 8.11 不要在公开应用中无限制使用用户邮箱

当前发送者是用户的 126 邮箱，公开访问者可以填写收件地址。如果没有访问控制、白名单和频率限制，可能导致垃圾邮件、额度耗尽或邮箱封禁。

## 9. 新会话开始时建议先做的检查

```powershell
cd "C:\Users\Administrator\Documents\New project for test\HelloGit"
git status -sb
git remote -v
git log -3 --oneline
python -m pytest tests -q
```

然后确认：

1. 用户这次要继续开发什么，不要自动扩大范围。
2. 云端应用是否仍能打开。
3. Streamlit Cloud Secrets 是否仍有效，但不要读取或回显真实值。
4. 应用是否准备公开；若是，优先完成安全限制。
5. `HANDOF.md` 是否需要提交到 GitHub，必须由用户决定。

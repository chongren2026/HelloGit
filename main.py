"""AI 科研助手的命令行入口。"""

from app.capabilities.mailer import send_excel_via_email, validate_email
from app.workflow import run_research


def main() -> None:
    topic = input("请输入研究主题：").strip()
    if not topic:
        print("研究主题不能为空。")
        return

    result = run_research(topic)
    print(f"Markdown 报告已生成：{result.report_path}")
    print(f"Excel 检索结果已生成：{result.excel_path}")

    recipient = input("请输入接收邮箱地址（直接回车跳过发送）：").strip()
    if not recipient:
        print("已跳过邮件发送。")
        return

    try:
        recipient = validate_email(recipient)
        if result.excel_path is None:
            raise RuntimeError("Excel 文件尚未生成")
        send_excel_via_email(recipient, result.excel_path, topic)
    except (ValueError, RuntimeError, FileNotFoundError, OSError) as exc:
        print(f"邮件发送失败：{exc}")
        return

    result.email_sent_to = recipient
    print(f"Excel 已发送至：{recipient}")


if __name__ == "__main__":
    main()

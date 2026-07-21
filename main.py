"""AI 科研助手的命令行入口。"""

from app.workflow import run_research


def main() -> None:
    topic = input("请输入研究主题：").strip()
    if not topic:
        print("研究主题不能为空。")
        return

    result = run_research(topic)
    print(f"报告已生成：{result.report_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
record_user_input.py - UserPromptSubmit Hook
记录用户输入到 memory78 每日日志

兼容: Claude Code / CodeBuddy
"""

import sys, os, json, subprocess
from datetime import datetime
from pathlib import Path

SKIP_PREFIXES = ("/m78", "/memory78", "/compact", "/todo", "/clear", "/cost", "/context", "/init")
SKIP_EXACT = ("", "y", "n", "yes", "no")
MAX_LEN = 500

PROJECT_DIR = Path(os.environ.get("CODEBUDDY_PROJECT_DIR", os.getcwd()))
DAILY_DIR = PROJECT_DIR / "memory78" / "system" / "static" / "daily"


def write_markdown(content: str):
    """直接写入 Markdown 文件"""
    date_str = datetime.now().strftime("%Y%m%d")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    md_file = DAILY_DIR / f"{date_str}.md"

    if md_file.exists():
        text = md_file.read_text(encoding="utf-8")
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if line.startswith("updated_at:"):
                new_lines.append(f"updated_at: {timestamp}")
            else:
                new_lines.append(line)
        md_file.write_text("\n".join(new_lines), encoding="utf-8")
    else:
        frontmatter = f"""---
title: {date_str}
tags: ["daily", "{date_str}"]
created_at: {timestamp}
updated_at: {timestamp}
apisys: system
apimicro: static
apiobj: daily
---

# {date_str}

"""
        md_file.write_text(frontmatter, encoding="utf-8")

    with open(md_file, "a", encoding="utf-8") as f:
        f.write(f"\n- [{timestamp}] {content}\n")


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = data.get("prompt", "").strip()
    if not prompt or prompt.lower() in SKIP_EXACT:
        sys.exit(0)
    for p in SKIP_PREFIXES:
        if prompt.startswith(p):
            sys.exit(0)

    if len(prompt) > MAX_LEN:
        prompt = prompt[:MAX_LEN] + "..."

    # 先试 m78 daily，失败则直接写 Markdown
    try:
        r = subprocess.run(["m78", "daily", prompt], capture_output=True, timeout=5)
        if r.returncode == 0:
            sys.exit(0)
    except Exception:
        pass

    write_markdown(prompt)
    sys.exit(0)


if __name__ == "__main__":
    main()

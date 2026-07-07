#!/usr/bin/env python3
"""
record_user_input.py - UserPromptSubmit Hook
等价于旧 Claude Code 的 record-user-input.sh

触发时机: 用户每次提交 prompt 时
功能:     调用 m78 daily 记录用户输入
"""

import sys, json

SKIP_PREFIXES = ("/m78", "/memory78", "/compact", "/todo", "/clear", "/cost", "/context", "/init")
SKIP_EXACT = ("", "y", "n", "yes", "no")

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

    # 截断
    if len(prompt) > 500:
        prompt = prompt[:500] + "..."

    import subprocess
    subprocess.run(["m78", "daily", prompt], capture_output=True)

    sys.exit(0)

if __name__ == "__main__":
    main()

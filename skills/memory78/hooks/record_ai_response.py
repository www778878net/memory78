#!/usr/bin/env python3
"""
record_ai_response.py - Stop Hook  
AI 回答完毕时，从 transcript 提取回复 → m78 daily
"""

import sys, json, subprocess
from pathlib import Path

MAX_LEN = 600

def extract_last_assistant_text(transcript_path: str) -> str:
    if not transcript_path or not Path(transcript_path).exists():
        return ""
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return ""

    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("role") != "assistant":
            continue

        content = msg.get("content", "")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            texts = []
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    t = block.get("text", "").strip()
                    if t:
                        texts.append(t)
                elif block.get("type") == "tool_use":
                    name = block.get("name", "?")
                    inp = block.get("input", {})
                    if isinstance(inp, dict):
                        fpath = inp.get("file_path") or inp.get("filePath") or ""
                        texts.append(f"[{name}] {fpath}" if fpath else f"[{name}]")
            return "\n".join(texts).strip() if texts else ""
    return ""

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    text = extract_last_assistant_text(data.get("transcript_path", ""))
    if not text:
        sys.exit(0)

    if len(text) > MAX_LEN:
        text = text[:MAX_LEN] + "\n...(已截断)"

    subprocess.run(["m78", "daily", f"🤖 {text}"], capture_output=True)
    sys.exit(0)

if __name__ == "__main__":
    main()

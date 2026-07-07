#!/usr/bin/env python3
"""
capture_session.py - SessionEnd Hook
会话结束时保存完整 transcript 到 memory78/traces/

存储: memory78/traces/{YYYYMM}/session-{时间}-{sid}.jsonl
"""

import sys
import os
import json
import shutil
from datetime import datetime
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")
    transcript_path = data.get("transcript_path", "")
    reason = data.get("reason", "other")

    # 持久化到 memory78/traces/
    project_dir = Path(os.environ.get("CODEBUDDY_PROJECT_DIR", "/workspace"))
    traces_dir = project_dir / "memory78" / "traces" / datetime.now().strftime("%Y%m")
    traces_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    source = Path(transcript_path)
    if not source.exists():
        sys.exit(0)

    dest_name = f"session-{timestamp}-{session_id[:8]}.jsonl"
    dest = traces_dir / dest_name
    shutil.copy2(source, dest)

    # 生成摘要
    try:
        lines = source.read_text(encoding="utf-8").strip().split("\n")
        user_count = sum(1 for l in lines if '"role":"user"' in l)
        bot_count = sum(1 for l in lines if '"role":"assistant"' in l)
        size_kb = source.stat().st_size / 1024

        summary = {
            "session_id": session_id,
            "captured_at": datetime.now().isoformat(),
            "reason": reason,
            "trace_file": str(dest),
            "stats": {
                "user_msgs": user_count,
                "assistant_msgs": bot_count,
                "lines": len(lines),
                "size_kb": round(size_kb, 1)
            }
        }
        summary_file = traces_dir / f"session-{timestamp}-{session_id[:8]}.summary.json"
        summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

    if os.environ.get("CODEBUDDY_HOOK_DEBUG"):
        print(f"[trace] {dest_name} → memory78/traces/", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()

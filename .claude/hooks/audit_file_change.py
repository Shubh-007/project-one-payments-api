import datetime
import json
import os
import sys
 
payload = json.load(sys.stdin)
os.makedirs(".claude/audit", exist_ok=True)
entry = {
    "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    "tool_name": payload.get("tool_name"),
    "file_path": (payload.get("tool_input") or {}).get("file_path"),
    "cwd": payload.get("cwd"),
}
with open(".claude/audit/file_changes.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")
 
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Audit log updated at .claude/audit/file_changes.jsonl"
    }
}))

import json
import re
import sys
 
payload = json.load(sys.stdin)
tool_name = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {}) or {}
text = json.dumps(tool_input)
file_path = tool_input.get("file_path", "")
 
is_edit_tool = tool_name in ["Edit", "Write", "MultiEdit"]
touches_legacy = "src/legacy" in file_path or "src/legacy" in text
has_ticket = re.search(r"AUD-\d+", text) is not None


if is_edit_tool and touches_legacy and not has_ticket:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Blocked: src/legacy changes require an AUD ticket such as AUD-114."
        }
    }))
    sys.exit(0)
 
sys.exit(0)

"""
MCP Server for Stack Trace Symbolic Fault Localizer Skill.
"""

import json
import sys
from client import FaultLocalizer

LOCALIZER = FaultLocalizer()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "parse_traceback",
                    "description": "Parse raw traceback string into structured frame objects and identify root cause",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "traceback_text": {"type": "string"}
                        },
                        "required": ["traceback_text"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "parse_traceback":
            res = LOCALIZER.parse_traceback(args["traceback_text"])
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

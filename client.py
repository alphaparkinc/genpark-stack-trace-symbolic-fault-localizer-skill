"""
Stack Trace Symbolic Fault Localizer Skill Client
Pure Python Standard Library implementation of Stack Trace Analysis and Spectrum-Based Fault Localization (SBFL).
Parses complex tracebacks into frame trees, extracts error tokens, and ranks suspect lines.
"""

import re
import math
from typing import List, Dict, Any, Tuple, Optional


class FaultLocalizer:
    """
    Parses traceback output and ranks suspicious source lines using Ochiai formula:
    Suspiciousness = failed(s) / sqrt(total_failed * (failed(s) + passed(s)))
    """

    FRAME_REGEX = re.compile(r'File "([^"]+)", line (\d+), in ([^\n]+)\n\s*(.+)')

    def parse_traceback(self, tb_text: str) -> Dict[str, Any]:
        """Parse raw Python exception traceback into structured frame list."""
        frames = []
        matches = self.FRAME_REGEX.findall(tb_text)

        for filename, lineno, func, code_line in matches:
            frames.append({
                "file": filename.strip(),
                "line": int(lineno),
                "function": func.strip(),
                "code": code_line.strip()
            })

        # Extract exception message (last line)
        lines = [l.strip() for l in tb_text.strip().splitlines() if l.strip()]
        exception_type = "Exception"
        exception_message = ""

        if lines:
            last_line = lines[-1]
            if ":" in last_line:
                parts = last_line.split(":", 1)
                exception_type = parts[0].strip()
                exception_message = parts[1].strip()
            else:
                exception_type = last_line

        # Root cause heuristic: innermost non-stdlib frame
        root_cause_frame = None
        for f in reversed(frames):
            if "<frozen" not in f["file"] and "lib/python" not in f["file"].lower():
                root_cause_frame = f
                break

        return {
            "exception_type": exception_type,
            "exception_message": exception_message,
            "frames": frames,
            "frame_depth": len(frames),
            "probable_root_cause": root_cause_frame
        }

    def compute_ochiai_suspiciousness(self, line_hits_failed: int, line_hits_passed: int, total_failed: int) -> float:
        """
        Ochiai metric for Spectrum-Based Fault Localization.
        """
        if total_failed == 0 or (line_hits_failed + line_hits_passed) == 0:
            return 0.0

        numerator = line_hits_failed
        denominator = math.sqrt(total_failed * (line_hits_failed + line_hits_passed))
        return round(numerator / denominator, 4) if denominator > 0 else 0.0

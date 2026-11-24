#!/usr/bin/env python3
"""Summarise a GitHub check-runs JSON listing: name, status, conclusion, minutes.

usage: checkruns.py FILE
"""

import datetime
import json
import sys


def when(text):
    """An ISO timestamp, or None."""
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00")) if text else None


def main() -> int:
    data = json.load(open(sys.argv[1]))
    print("total", data["total_count"])
    for run in sorted(data["check_runs"], key=lambda r: r["name"]):
        start, end = when(run["started_at"]), when(run["completed_at"])
        minutes = round((end - start).total_seconds() / 60, 1) if start and end else "-"
        print(f"{run['name']:<45} {run['status']:<12} {str(run['conclusion']):<10} {minutes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

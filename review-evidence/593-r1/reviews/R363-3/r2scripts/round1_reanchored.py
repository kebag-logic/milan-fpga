#!/usr/bin/env python3
"""R363-2: my round-1 mutants whose anchors no longer exist, re-anchored to the head code
that now implements the same rule. Usage as reviewer_mutants.py (same runner)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reviewer_mutants as runner  # noqa: E402

runner.MUTANTS = (
    ("R1-M01r mr cause check skipped",
     '        if not matches:\n            return "FAIL", {"why": "mr toggle without a recorded media-clock cause", "toggle": toggle}',
     '        if False:\n            return "FAIL", {"why": "mr toggle without a recorded media-clock cause", "toggle": toggle}'),
    ("R1-M14r counter decrease decoded as wrap (superseded by reset classification)",
     '        if after["value"] < before["value"]:\n            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",\n                            "before": before["value"], "after": after["value"]}\n        delta = after["value"] - before["value"]',
     '        delta = (after["value"] - before["value"]) % 2**32'),
    ("R1-M26r history interval-grading list counts a GM change at the clear instant (verdict-equivalent: the uncovered-GM loop still fails it; that loop's own <= is round-2 M02)",
     "if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "if start_s - resolution_s <= Decimal(str(event)) <= clear_s]"),
    ("R1-M40r first toggle exempt from cause",
     "    for toggle in toggles:\n        matches =", "    for toggle in toggles[1:]:\n        matches ="),
    ("R1-M41r last toggle exempt from cause",
     "    for toggle in toggles:\n        matches =", "    for toggle in toggles[:-1]:\n        matches ="),
    ("R1-M48r single entry ignores GM before observed start",
     "    gm_events_s = gm_changes_s\n",
     "    gm_events_s = [event_s for event_s in gm_changes_s if observed_start_s <= event_s]\n"),
    ("R1-M48h history ignores GM before observed start when grading an interval",
     "        covered_gm_s = [event for event in gm_changes_s\n                        if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "        covered_gm_s = [event for event in gm_changes_s\n                        if start_s <= Decimal(str(event)) < clear_s]"),
)

if __name__ == "__main__":
    raise SystemExit(runner.main())

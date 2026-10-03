#!/usr/bin/env python3
"""Replay the published A/B gate records through the head's comparator.

Usage: replay_records.py <repo checkout> <evidence dir holding *-record-*.json>
Judges each published record against the head's pp_resource_baseline.json
endpoint with pp_resource_gate.judge and prints the verdict and the report.
"""
import json
from pathlib import Path
import sys

repo, ev = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_resource_gate as gate  # noqa: E402

base = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
for record, endpoint in (("A-record-route-1x1", "route-1x1"), ("A-record-ooc-1x1", "ooc-1x1"),
                         ("A-record-ooc-8x8", "ooc-8x8"), ("B-record-route-1x1", "route-1x1"),
                         ("B-record-ooc-1x1", "ooc-1x1"), ("B-record-ooc-8x8", "ooc-8x8"),
                         ("A-record-ooc-1x1-10ns", "ooc-1x1")):
    candidate = json.loads((ev / f"{record}.json").read_text())
    status, lines = gate.judge(base[endpoint], candidate)
    print(f"=== {record} against {endpoint}: exit {status}")
    print("\n".join(lines))

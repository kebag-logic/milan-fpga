#!/usr/bin/env python3
"""Judge published A/B records against the committed record with the gate's own judge().

R447-9 probe for issue #234 / PR #638. Read-only: imports the gate from the
clone at the reviewed head and never writes into it.
Usage: judge_against_record.py REPO RECORDS_DIR
"""
import json
import sys
from pathlib import Path

repo, records = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "syn/ooc"))
sys.dont_write_bytecode = True
import pp_resource_gate as gate  # noqa: E402

baseline = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())
cases = [(s, ep, f"{s}-record-{ep}.json") for s in ("A", "B") for ep in ("route-1x1", "ooc-1x1", "ooc-8x8")]
cases.append(("A", "ooc-1x1", "A-record-ooc-1x1-10ns.json"))
for label, endpoint, name in cases:
    candidate = json.loads((records / name).read_text())
    if "record" in candidate and "kind" not in candidate:
        candidate = candidate["record"]
    unrouted = [] if endpoint.startswith("route") else None
    rc, lines = gate.judge(baseline["endpoints"][endpoint], candidate, unrouted)
    print(f"== {name} against committed {endpoint}: rc {rc}")
    for line in lines[:4]:
        print("   " + line)

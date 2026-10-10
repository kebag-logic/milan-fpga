#!/usr/bin/env python3
"""Compare MARK_II_AREA_PLAN.md's current processor inventory with the record.

Usage: python3 -I check_mark2_inventory.py <repo-root>
Each table row `| `scope` | route | ooc-1x1 | ooc-8x8 | ... |` in the
"Current processor inventory" section must equal the LUT figure of that scope
in syn/ooc/pp_resource_baseline.json's three record objects. Also prints the
route-1x1 headline figures. Exit 1 on any mismatch or if no row is found.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
endpoints = json.loads((root / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
scopes = [endpoints[name]["record"]["scopes"] for name in ("route-1x1", "ooc-1x1", "ooc-8x8")]
print("route-1x1 figures:", json.dumps(endpoints["route-1x1"]["record"]["figures"]))
text = (root / "docs/design/MARK_II_AREA_PLAN.md").read_text().split("### Current processor inventory", 1)[1]
text = text.split("\n## ", 1)[0]
rows = bad = 0
for line in text.splitlines():
    match = re.match(r"\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", line)
    if not match:
        continue
    rows += 1
    page = [int(v.replace(",", "")) for v in match.group(2, 3, 4)]
    record = [s.get(match.group(1), {}).get("LUT") for s in scopes]
    verdict = "OK" if page == record else "MISMATCH"
    bad += verdict != "OK"
    print(f"{verdict} {match.group(1)} page={page} record={record}")
print(f"rows: {rows}  figures: {3 * rows}  mismatches: {bad}")
sys.exit(1 if bad or not rows else 0)

#!/usr/bin/env python3
"""readme-counts.py <README.md> <campaign log>: every arm's failing-check count in the campaign log against its
`Failing checks` cell in the README's arm table; prints each mismatch and a total, exit 1 on any mismatch."""
import re
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
log = Path(sys.argv[2]).read_text()
cells = {m[0]: int(m[1]) for m in re.findall(r"^\| `([a-z0-9-]+)` \|.*\| (\d+) \|$", readme, re.M)}
runs = {m[0]: (int(m[1]), m[2]) for m in re.findall(r"^([a-z0-9-]+): rc=\d+ failures=(\d+) named=\d+ (\w+)", log, re.M)}
bad = 0
for arm, (n, verdict) in runs.items():
    if arm not in cells:
        print(f"NO README ROW {arm} ({n} failures, {verdict})"); bad += 1
    elif cells[arm] != n:
        print(f"MISMATCH {arm}: README {cells[arm]}, campaign {n}"); bad += 1
print(f"{len(runs)} arms in the log, {sum(1 for a in runs if a in cells)} with a README row, {bad} problems")
sys.exit(1 if bad else 0)

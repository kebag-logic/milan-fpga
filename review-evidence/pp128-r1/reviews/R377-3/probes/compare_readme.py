#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Compare the tb/acmp_talker/README.md campaign table with a retry_mutants.py log directory:
failure count equal, and the named assertion (prefix) present among the mutant's failures.
Usage: compare_readme.py README.md LOGDIR  (rc 0 iff every row matches and every logged mutant has a row)"""
import re, sys
from pathlib import Path
readme, logs = Path(sys.argv[1]).read_text(), Path(sys.argv[2])
rows = re.findall(r"^\| `([a-z0-9_]+)` \| ([^|]+) \| ([^|]+) \|$", readme, re.M)
bad = 0; seen = set()
for name, verdict, first in rows:
    seen.add(name)
    log = logs / f"{name}.txt"
    if not log.exists():
        print(f"NO-LOG   {name}"); bad += 1; continue
    text = log.read_text().splitlines()
    rc = int(text[0].split(":")[1]); fails = [l[len("FAIL: "):] for l in text if l.startswith("FAIL: ")]
    m = re.match(r"killed, (\d+) failures", verdict.strip())
    if m:
        ok = rc != 0 and len(fails) == int(m.group(1)) and any(f.startswith(first.strip()) for f in fails)
        got = f"rc={rc} n={len(fails)} named-present={any(f.startswith(first.strip()) for f in fails)}"
    else:
        ok = rc == 0 and not fails and ("control" in verdict)
        got = f"rc={rc} n={len(fails)}"
    print(f"{'MATCH' if ok else 'DIFF '}    {name:32s} readme=[{verdict.strip()} | {first.strip()}] rerun=[{got}]")
    bad += not ok
extra = sorted(p.stem for p in logs.glob("*.txt") if p.stem not in seen | {"baseline", "restored", "coverage"})
for e in extra: print(f"NO-ROW   {e}"); bad += 1
print(f"rows={len(rows)} mismatches={bad}")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Compare tb/maap/README.md's mutation ledger tallies with a campaign run's logs.

usage: check_ledger.py <README.md> <campaign log dir>
Each ledger row ends "N FAIL of M"; the arm's log for that suite must end with
the tally (M checks, N FAIL). Also prints each arm's U29 FAIL lines.
"""
import re
import sys
from pathlib import Path

readme, logs = Path(sys.argv[1]), Path(sys.argv[2])
TALLY = re.compile(r"(\d+) checks: \d+ PASS, (\d+) FAIL|\] (\d+) checks, (\d+) failures")
rows = []
label = None
for line in readme.read_text().splitlines():
    m = re.match(r"\| `([a-z0-9-]+)` \|.*\| (maap|rx_validator|pp_top[^|]*) \|.*?(\d[\d,]*) FAIL of (\d[\d,]*) \|$", line)
    same = re.match(r"\| \(same arm\) \|.*\| (maap|rx_validator|pp_top[^|]*) \|.*?(\d[\d,]*) FAIL of (\d[\d,]*) \|$", line)
    if m:
        label = m.group(1)
        rows.append((label, m.group(2).split()[0], int(m.group(3).replace(',', '')), int(m.group(4).replace(',', ''))))
    elif same and label:
        rows.append((label, same.group(1).split()[0], int(same.group(2).replace(',', '')), int(same.group(3).replace(',', ''))))
bad = 0
for label, suite, nfail, total in rows:
    log = logs / f"{label}-{suite}.log"
    if not log.exists():
        print(f"MISSING {label} [{suite}]")
        bad += 1
        continue
    text = log.read_text()
    found = TALLY.findall(text)[-1]
    got = (int(found[0]), int(found[1])) if found[0] else (int(found[2]), int(found[3]))
    ok = got == (total, nfail)
    bad += not ok
    u29 = [l for l in text.splitlines() if l.startswith("FAIL: U29")]
    print(f"{'OK  ' if ok else 'DIFF'} {label} [{suite}] ledger {nfail} of {total}, log {got[1]} of {got[0]}"
          + (f"; U29 FAILs {len(u29)}" if u29 else ""))
    for l in u29:
        print(f"       {l}")
print(f"{len(rows)} ledger rows, {bad} mismatches")
sys.exit(1 if bad else 0)

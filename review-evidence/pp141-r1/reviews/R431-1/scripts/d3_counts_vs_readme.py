#!/usr/bin/env python3
"""Compare each d3_mutants.py log's failing-check count with the README row.

Usage: d3_counts_vs_readme.py README OUTDIR [OUTDIR ...]
Reads every <mutant>.log in each OUTDIR (golden logs skipped), takes the
"D3: N checks, M failures" tally (or the "N checks: P PASS, F FAIL" tally of
other suites), and compares M with the last column of the README's table row
for that mutant. Exit 0 only if every compared count agrees.
"""
import re
import sys
from pathlib import Path

readme = Path(sys.argv[1]).read_text()
rows = {}
for line in readme.splitlines():
    m = re.match(r"^\| `([A-Za-z0-9_]+)` \|.*\| (\d+) \|\s*$", line)
    if m:
        rows.setdefault(m.group(1), int(m.group(2)))
rc = 0
for out in sys.argv[2:]:
    for log in sorted(Path(out).glob("*.log")):
        name = log.stem
        if name.startswith("golden"):
            continue
        text = log.read_text(errors="replace")
        t = re.findall(r"^D3: (\d+) checks, (\d+) failures$", text, re.M)
        fails = int(t[-1][1]) if t else None
        if fails is None:
            t2 = re.findall(r"^(\d+) checks: \d+ PASS, (\d+) FAIL$", text, re.M)
            fails = int(t2[-1][1]) if t2 else None
        rec = rows.get(name)
        ok = fails is not None and rec is not None and fails == rec
        if not ok:
            rc = 1
        print(f"{name}: measured={fails} readme={rec} {'AGREE' if ok else 'DIFFER'}")
sys.exit(rc)

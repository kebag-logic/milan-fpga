#!/usr/bin/env python3
"""Compare a MAAP campaign log's per-arm tallies with tb/maap/README.md's ledger rows, keyed by (arm, suite).
Usage: 40-ledger-compare.py <README.md> <campaign log>"""
import re
import sys

readme, log = sys.argv[1], sys.argv[2]
rows = {}
label = None
text = open(readme).read()
sect = text[text.index("## Mutation campaign"):]
for line in sect.splitlines():
    m = re.search(r"(\d+) FAIL of (\d+) \|\s*$", line)
    if m and line.startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        named = re.match(r"`([^`]+)`", cells[0])
        label = named.group(1) if named else label  # "(same arm)" inherits
        suite = cells[2].split()[0].strip("`")
        rows[(label, suite)] = (int(m.group(1)), int(m.group(2)))
runs = []
for line in open(log):
    m = re.match(r"(\S+) \[(\S+)\]: rc=\d+ tally=\((\d+), (\d+)\) named=\d+ (KILLED|UNPROVEN)", line)
    if m:
        runs.append((m.group(1), m.group(2), int(m.group(4)), int(m.group(3)), m.group(5)))
bad = 0
print(f"ledger rows {len(rows)}, campaign arm runs {len(runs)}")
for label, suite, fails, total, verdict in runs:
    lf, lt = rows.get((label, suite), (None, None))
    ok = verdict == "KILLED" and (fails, total) == (lf, lt)
    bad += not ok
    print(f"{'EQ ' if ok else 'NE '} {label:38s} {suite:12s} run {fails} FAIL of {total}  ledger {lf} of {lt}")
bad += len(rows) != len(runs)
print("ALL EQUAL" if not bad else f"{bad} MISMATCH")
sys.exit(1 if bad else 0)

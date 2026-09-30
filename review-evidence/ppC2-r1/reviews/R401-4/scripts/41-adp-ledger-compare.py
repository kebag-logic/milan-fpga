#!/usr/bin/env python3
"""Compare an ADP campaign log's per-arm failure counts with tb/adp_engine/README.md's ledger.
Usage: 41-adp-ledger-compare.py <README.md> <campaign log>"""
import re
import sys

ledger = {}
for line in open(sys.argv[1]):
    m = re.match(r"\| `([^`]+)` \| ([^|]+) \| .*\| (\d+)[:\s]", line)
    if m:
        ledger[m.group(1)] = int(m.group(3))
bad = 0
seen = 0
for line in open(sys.argv[2]):
    m = re.match(r"(\S+): rc=\d+ failures=(\d+) named=\d+ (KILLED|UNPROVEN)", line)
    if m:
        seen += 1
        want = ledger.get(m.group(1))
        ok = m.group(3) == "KILLED" and want == int(m.group(2))
        bad += not ok
        print(f"{'EQ ' if ok else 'NE '} {m.group(1):36s} run {m.group(2)} ledger {want}")
bad += seen != len(ledger)
print(f"ledger arms {len(ledger)}, campaign arms {seen}: {'ALL EQUAL' if not bad else str(bad) + ' MISMATCH'}")
sys.exit(1 if bad else 0)

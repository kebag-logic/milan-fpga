#!/usr/bin/env python3
"""Cross-check the milan_dp README dynmap campaign table against a campaign verdicts file.
Usage: python3 -I table_vs_verdicts.py <README.md> <verdicts.txt>"""
import re, sys
rows = {}
for line in open(sys.argv[1]):
    m = re.match(r"^\| (\d+) \| ([^|]+) \| (.+?) \| (.+) \| (\d+) of (\d+) \|$", line.rstrip())
    if m: rows[int(m.group(1))] = (m.group(3).strip(), int(m.group(5)), int(m.group(6)))
ver = []
for line in open(sys.argv[2]):
    m = re.match(r"^\[(PASS|FAIL)\] mutant caught: (.+?) - breaks .*\(its tallies report (\d+) failure\(s\) across (\d+) checks\)", line)
    if m: ver.append((m.group(1), m.group(2), int(m.group(3)), int(m.group(4))))
bad = 0
print(f"table rows {len(rows)}, verdict lines {len(ver)}")
for i, (st, name, f, n) in enumerate(ver, 1):
    r = rows.get(i)
    ok = st == "PASS" and r is not None and r[0] == name and (r[1], r[2]) == (f, n)
    if not ok: bad += 1; print("MISMATCH", i, r, (st, name, f, n))
print("mismatches", bad)
sys.exit(1 if bad or len(rows) != len(ver) else 0)

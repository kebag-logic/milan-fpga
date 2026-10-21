#!/usr/bin/env python3
"""Compare two campaign verdict files mutant by mutant: name and failure count (leg total ignored).
Usage: python3 -I failure_counts.py <verdicts A> <verdicts B>"""
import re, sys
def rd(p):
    rx = re.compile(r"^\[(PASS|FAIL)\] mutant caught: (.+?) - breaks .*report (\d+) failure\(s\) across (\d+) checks")
    return [(m.group(1), m.group(2), int(m.group(3)), int(m.group(4))) for m in map(rx.match, open(p)) if m]
a, b = rd(sys.argv[1]), rd(sys.argv[2])
diff = [(x, y) for x, y in zip(a, b) if x[:3] != y[:3]]
print(f"A {len(a)} rows, B {len(b)} rows, rows whose verdict, name or failure count differ: {len(diff)}")
for x, y in diff: print("  ", x, "->", y)
sys.exit(1 if diff or len(a) != len(b) else 0)

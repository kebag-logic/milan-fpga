#!/usr/bin/env python3
"""Every GoogleTest TEST/TEST_F/TEST_P name under sw/firmware/ctrl/test at a base checkout must be defined at
the head, in sw/firmware/ctrl/test or in third_party/tsn-c-stack/tests. Usage: test_inventory.py <base> <head>"""
import re, sys
from pathlib import Path
R = re.compile(r'^\s*TEST(?:_F|_P)?\(\s*(\w+)\s*,\s*(\w+)\s*\)', re.M)
def names(*dirs):
    out = {}
    for d in dirs:
        for f in sorted(Path(d).glob('*.cpp')):
            for s, n in R.findall(f.read_text(errors='replace')):
                out.setdefault(f"{s}.{n}", []).append(f.name)
    return out
b = names(Path(sys.argv[1]) / 'sw/firmware/ctrl/test')
h = names(Path(sys.argv[2]) / 'sw/firmware/ctrl/test', Path(sys.argv[2]) / 'third_party/tsn-c-stack/tests')
lost = sorted(set(b) - set(h)); new = sorted(set(h) - set(b))
moved = sorted(n for n in b if n in h and set(b[n]) != set(h[n]))
print(f"base tests {len(b)}; head tests {len(h)}; lost {len(lost)}; new {len(new)}; moved file {len(moved)}")
for n in lost: print("LOST", n, b[n])
for n in new: print("NEW", n, h[n])
sys.exit(1 if lost else 0)

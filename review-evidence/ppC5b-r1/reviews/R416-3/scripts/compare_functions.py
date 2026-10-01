#!/usr/bin/env python3
"""Compare named top-level C++ functions (from their '//!' doc lines through
the closing '}' at column 0) between two revisions of tb/pp_top/sim_main.cpp.
Usage: compare_functions.py REPO REV_A REV_B NAME [NAME ...]"""
import subprocess, sys
repo, a, b, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def body(rev, name):
    t = subprocess.run(['git', '-C', repo, 'show', f'{rev}:tb/pp_top/sim_main.cpp'],
                       capture_output=True, text=True, check=True).stdout.split('\n')
    s = next((i for i, l in enumerate(t) if f' {name}(H& h)' in l and l.rstrip().endswith('{')), None)
    if s is None: return None
    e = next(i for i in range(s, len(t)) if t[i] == '}')
    return t[s:e + 1]
for n in names:
    x, y = body(a, n), body(b, n)
    print(f"{n}: {a[:8]} {len(x) if x else 'absent'} lines, {b[:8]} {len(y) if y else 'absent'} lines, "
          f"{'IDENTICAL' if x == y and x else 'DIFFERENT'}")

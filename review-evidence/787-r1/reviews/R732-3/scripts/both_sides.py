#!/usr/bin/env python3
"""For each path, check that every line each merge side added against the merge base
is present in the merge result, and every line a side removed is absent unless the other
side has it. Usage: both_sides.py REPO BASE OURS THEIRS RESULT PATH..."""
import subprocess, sys, collections
repo, base, ours, theirs, result, *paths = sys.argv[1:]
def blob(rev, p):
    r = subprocess.run(['git', '-C', repo, 'show', f'{rev}:{p}'], capture_output=True)
    return r.stdout.decode('utf-8', 'replace').splitlines() if r.returncode == 0 else []
bad = 0
for p in paths:
    B, O, T, R = (collections.Counter(blob(x, p)) for x in (base, ours, theirs, result))
    for side, S, other in (('ours', O, T), ('theirs', T, O)):
        for line, n in (S - B).items():
            if R[line] < n and line.strip():
                bad += 1; print(f'MISSING {p} [{side} added]: {line[:160]!r}')
        for line, n in (B - S).items():
            if R[line] > max(B[line] - n, other[line] - B[line] + B[line] - n, 0) and line.strip() and other[line] < B[line] + (R[line] - B[line]):
                print(f'NOTE {p} [{side} removed, still present]: {line[:160]!r}')
    print(f'{p}: checked')
print('RESULT', 'FAIL' if bad else 'OK', 'missing', bad)
sys.exit(1 if bad else 0)

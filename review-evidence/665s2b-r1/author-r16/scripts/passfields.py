#!/usr/bin/env python3
"""One window's work passes from MARK composed to UNTIL ms, each with its counters (no module list).
usage: passfields.py LOG [UNTIL_MS]"""
import re, sys
lines = open(sys.argv[1], errors='replace').read().splitlines()
until = float(sys.argv[2]) if len(sys.argv) > 2 else 19
start = next(int(l.split()[1]) for l in lines if re.fullmatch(r'MARK \d+ composed', l))
for l in lines:
    if l.startswith('PASS '):
        k = l.split(' W ')[0].split()
        t = (int(k[2]) - start) / 1e5
        if 0 <= t <= until:
            print(f'{t:+8.3f} ' + ' '.join(x for x in k[4:] if not x.startswith('mods=') and not x.startswith('code_words')))

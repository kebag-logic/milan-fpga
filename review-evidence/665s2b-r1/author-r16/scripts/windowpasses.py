#!/usr/bin/env python3
"""The passes of one save window (#665): from 3 ms before it opens (MARK composed) to its last record's release,
each work pass (PASS) and each pass that carries the store's step (STEPPASS, aged or not) with its start after the
opening, CPU cycles and its four costliest modules, and each TICK record posted, so an aged step's place and cost in
the window can be read; a run of passes that wrote nothing to the mailbox is one IDLE line.

usage: windowpasses.py LOG [UNTIL_MS]
"""
import re
import sys

text = open(sys.argv[1], errors='replace').read().splitlines()
until = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
start = next(int(l.split()[1]) for l in text if re.fullmatch(r'MARK \d+ composed', l))
hz = 100_000_000
at = lambda c: (c - start) * 1000 / hz
lo, hi = start - 3 * hz // 1000, start + int(until * hz / 1000)
for line in text:
    k = line.split()
    if not k:
        continue
    if k[0] in ('PASS', 'STEPPASS') and lo <= int(k[2]) <= hi:
        extra = ''
        if k[0] == 'PASS':
            mods = dict(x.split('=', 1) for x in line.split(' W')[0].split()[5:] if '=' in x).get('mods', '')
            top = sorted(((int(m.split(':')[1]), m.split(':')[0]) for m in mods.split(',') if m), reverse=True)[:4]
            extra = ' '.join(f'{n}:{c}' for c, n in top) + (' step' if ' step=1 ' in line else '')
        else:
            extra = ' '.join(k[5:])
        print(f'{k[0]:8s} {at(int(k[2])):+8.3f} ms {int(k[4]):8,d} {extra}')
    elif k[0] == 'EVW' and int(k[2]) % 4 == 0 and int(k[3], 16) & 0xFF == 4 and lo <= int(k[1]) <= hi:
        print(f'TICK     {at(int(k[1])):+8.3f} ms')
    elif k[0] == 'MARK' and lo <= int(k[1]) <= hi:
        print(f'MARK     {at(int(k[1])):+8.3f} ms {k[2]}')

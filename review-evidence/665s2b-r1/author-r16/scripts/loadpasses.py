#!/usr/bin/env python3
"""The passes of a held group from a mark (default notice.load) to UNTIL ms after it (#665): each work pass (PASS)
and each pass that carries the store's step (STEPPASS), with its start after the mark, CPU cycles and its costliest
modules, the receive commits (RXC, per channel) and TICK records between passes, so a burst's drain can be read.

usage: loadpasses.py LOG [UNTIL_MS] [MARK] [TOP]
"""
import re
import sys

text = open(sys.argv[1], errors='replace').read().splitlines()
until = float(sys.argv[2]) if len(sys.argv) > 2 else 22.0
mark = sys.argv[3] if len(sys.argv) > 3 else 'notice.load'
top_n = int(sys.argv[4]) if len(sys.argv) > 4 else 5
start = next(int(l.split()[1]) for l in text if re.fullmatch(rf'MARK \d+ {re.escape(mark)}', l))
hz = 100_000_000
at = lambda c: (c - start) * 1000 / hz
hi = start + int(until * hz / 1000)
rxc = {}
for line in text:
    k = line.split()
    if not k:
        continue
    if k[0] == 'RXC' and start <= int(k[1]) <= hi:
        rxc[k[2]] = rxc.get(k[2], 0) + 1
        continue
    if k[0] in ('PASS', 'STEPPASS') and start <= int(k[2]) <= hi:
        if rxc:
            print('         RXC ' + ' '.join(f'ch{c}:{n}' for c, n in sorted(rxc.items())))
            rxc = {}
        extra = ''
        if k[0] == 'PASS':
            mods = line.split(' mods=')[1].split(' W')[0]
            top = sorted(((int(m.split(':')[1]), m.split(':')[0]) for m in mods.split(',') if m), reverse=True)[:top_n]
            extra = ' '.join(f'{n}:{c}' for c, n in top) + (' STEP' if ' step=1 ' in line else '') + \
                (' AGED' if ' aged=1' in line else '')
        else:
            extra = ' '.join(k[5:])
        print(f'{k[0]:8s} {at(int(k[2])):+8.3f} {int(k[4]):8,d} {extra}')
    elif k[0] == 'EVW' and int(k[2]) % 4 == 0 and int(k[3], 16) & 0xFF == 4 and start <= int(k[1]) <= hi:
        print(f'TICK     {at(int(k[1])):+8.3f}')
    elif k[0] == 'MARK' and start <= int(k[1]) <= hi:
        print(f'MARK     {at(int(k[1])):+8.3f} {k[2]}')

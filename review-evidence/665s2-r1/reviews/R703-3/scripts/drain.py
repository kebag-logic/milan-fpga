#!/usr/bin/env python3
"""Per-pass RX_TAIL releases per channel inside a group's composed window, from the raw log.
Usage: drain.py CHECKOUT LOG"""
import sys
sys.path.insert(0, sys.argv[1] + '/sw/mailbox')
from mailbox_model import load
c = load()
chreg = {r.name: r.offset for r in c.ch_registers}
names = [x.name for x in c.channels]
tails = {(c.ch_base + n * c.ch_stride + chreg['RX_TAIL']) // 4: names[n] for n in range(len(names))}
lines = open(sys.argv[2]).read().splitlines()
marks = {l.split()[2]: int(l.split()[1]) for l in lines if l.startswith('MARK')}
t0, t1 = marks['composed'], marks['composed_end']
print(f'composed window {(t1 - t0) / 1e5:.2f} ms; token refill (contract): adp 1/10 ms, acmp 1/5 ms, aecp 1/5 ms, maap 1/20 ms')
total = {}
for l in lines:
    if not l.startswith('PASS'):
        continue
    f = l.split(); s = int(f[2]); cyc = int(f[4])
    if not t0 <= s <= t1:
        continue
    rel = {}
    for x in (l.split(' W', 1)[1].split() if ' W' in l else []):
        word = int(x.split(':')[1], 16)
        if word in tails:
            rel[tails[word]] = rel.get(tails[word], 0) + 1
    for k, v in rel.items():
        total[k] = total.get(k, 0) + v
    print(f'  pass at {(s - t0) / 1e5:8.2f} ms lasting {cyc / 5e4:6.2f} ms releases {rel}')
print('total releases', total)

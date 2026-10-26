#!/usr/bin/env python3
"""Every RX_TAIL write the firmware makes must land on a record boundary computed as
header words + ceil(frame bytes / 4) per committed record (mod 2^16): the accounting
grade.releases() assumes. Counts writes on and off a boundary per channel.
Usage: tail_boundaries.py CHECKOUT LOG..."""
import sys
sys.path.insert(0, sys.argv[1] + '/sw/mailbox')
from mailbox_model import load  # noqa: E402
c = load()
names = [x.name for x in c.channels]
reg = {r.name: r.offset for r in c.ch_registers}
tail = {(c.ch_base + n * c.ch_stride + reg['RX_TAIL']) // 4: n for n in range(len(names))}
H = len(c.rx_header)
on = off = 0
for path in sys.argv[2:]:
    bounds = {n: {0} for n in range(len(names))}
    acc = {n: 0 for n in range(len(names))}
    size = 0
    for l in open(path):
        f = l.split()
        if not f:
            continue
        if f[0] == 'RXS':
            size = int(f[3])
        elif f[0] == 'RXC':
            n = int(f[2])
            acc[n] += H + (size + 3) // 4
            bounds[n].add(acc[n] & 0xFFFF)
        elif f[0] == 'PASS' and ' W' in l:
            for w in l.split(' W', 1)[1].split():
                cyc, word, val = w.split(':')
                n = tail.get(int(word, 16))
                if n is not None:
                    if int(val, 16) in bounds[n]:
                        on += 1
                    else:
                        off += 1
                        print('OFF', path.split('/')[-1], names[n], val)
print(f'RX_TAIL writes on a record boundary: {on}; off: {off}')

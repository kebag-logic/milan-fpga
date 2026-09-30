#!/usr/bin/env python3
"""Re-derive the McASP0 receive DMA rate from the published SoC status logs.

Usage: mcasp_rx_rate.py <author-packet-dir>
Each status log holds two /proc/uptime reads that bracket one
/proc/interrupts read. The rate is computed with every uptime pairing, so
the consistent brackets (first-first, second-second) can be told from the
inconsistent ones (second-of-before to first-of-after, and the reverse).
"""
import hashlib, re, sys
from pathlib import Path

UP = re.compile(r'^(\d+\.\d+) \d+\.\d+$')
IRQ = re.compile(r'^\s*(\d+):\s+(\d+)\s+\d+\s+\d+\s+\d+\s+MSI-INTA\s+\d+\s+(Edge|Level)\s+(\S+) (chan\d)$')

def parse(p):
    ups, irq = [], {}
    for line in p.read_text().splitlines():
        m = UP.match(line)
        if m:
            ups.append(float(m.group(1)))
        m = IRQ.match(line)
        if m:
            irq[(m.group(4), m.group(5), m.group(3))] = int(m.group(2))
    return ups, irq

root = Path(sys.argv[1])
for run in ('usb-long', 'usb-long2'):
    b, a = root / 'runs' / run / 'soc-status-before.log', root / 'runs' / run / 'soc-status-after.log'
    for f in (b, a):
        print(f'{run} {f.name} sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}')
    ub, ib = parse(b)
    ua, ia = parse(a)
    assert len(ub) == 2 and len(ua) == 2, (ub, ua)
    key = ('485c0100.dma-controller', 'chan1', 'Edge')
    lkey = ('485c0100.dma-controller', 'chan1', 'Level')
    d = ia[key] - ib[key]
    dl = ia[lkey] - ib[lkey]
    print(f'{run} uptimes before {ub} after {ua}')
    print(f'{run} chan1 Edge {ib[key]} -> {ia[key]} delta {d}; chan1 Level delta {dl}')
    for name, i, j in (('first-first (consistent)', 0, 0), ('second-second (consistent)', 1, 1),
                       ('before-second to after-first (short)', 1, 0), ('before-first to after-second (long)', 0, 1)):
        t = ua[j] - ub[i]
        print(f'{run}   {name}: interval {t:.2f} s, {d / t:.3f} periods/s, {d * 192 / t:.1f} frames/s')

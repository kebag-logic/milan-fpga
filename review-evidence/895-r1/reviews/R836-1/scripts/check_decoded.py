#!/usr/bin/env python3
"""Reviewer's checks over decode_wire.py output. usage: check_decoded.py DECODED BASE_HEX N_IF [--window-ms 15000]
Checks: no Talker attribute before the first srp.talker_declare mark; no Talker Failed; every Talker of StreamID
...0100nn on interface nn % N_IF with DA = BASE + nn; after each source's Leave no declaring event (New/JoinIn/JoinMt)
of that source; reports each source's first Advertise and its Leave relative to its probe mark."""
import sys, re
dec, base, nif = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])
first_probe = None; probe = {}; fails = 0; first = {}; lv = {}; after_lv = {}; talker_before = 0; failed = 0; wrong = 0
for line in open(dec):
    m = re.match(r'\s*([\d.]+) MARK srp\.talker_declare\.s(\d+)\.if(\d+)', line)
    if m:
        t = float(m.group(1)); probe[int(m.group(2))] = t
        first_probe = t if first_probe is None else first_probe
        continue
    m = re.match(r'\s*([\d.]+) if(\d+) MSRP (Talker\w+) sid ([0-9a-f]{16}) DA ([0-9a-f]{12}) .* (New|JoinIn|In|JoinMt|Mt|Lv)', line)
    if not m:
        continue
    t, i, kind, sid, da, ev = float(m.group(1)), int(m.group(2)), m.group(3), m.group(4), int(m.group(5), 16), m.group(6)
    n = int(sid[-4:], 16)
    if first_probe is None or t < first_probe: talker_before += 1
    if kind == 'TalkerFailed': failed += 1
    if i != n % nif or da != base + n: wrong += 1; print('WRONG', line.strip())
    if ev == 'Lv':
        lv.setdefault(n, t)
    elif n in lv:
        after_lv[n] = after_lv.get(n, 0) + 1; print('AFTER-LEAVE', line.strip())
    elif ev == 'New':
        first.setdefault(n, (t, i))
for n in sorted(set(first) | set(lv)):
    p = probe.get(n); f = first.get(n); l = lv.get(n)
    print(f"s{n}: probe {p} first Advertise {f} (+{(f[0]-p) if f and p else None:.3f} ms) Leave {l} "
          f"({(l-p) if l and p else None} ms after probe)")
print(f"talker before first probe {talker_before}; talker failed {failed}; wrong interface/DA {wrong}; "
      f"declarations after a Leave {sum(after_lv.values())}")
sys.exit(1 if talker_before or failed or wrong or after_lv else 0)

"""Worst legal packetizer load per engine at each rate: every multiset of 16
base formats per port (both ports alike) within the 75 % class A cap, with
and without one CRF per port. Cycles at 50 MHz per the stream-engine page."""
import itertools
from fractions import Fraction as Fr
FORMATS = (1, 2, 4, 6, 8)
for khz, ns in ((48, 6), (96, 12), (192, 24)):
    res = {n: 8 * (max(24 + ns * 4 * n + 1 + 22, 68) + 20) for n in FORMATS}
    cyc = {n: 16 + ns * n for n in FORMATS}
    best = None
    for crf in (True, False):
        for combo in itertools.combinations_with_replacement(FORMATS, 16):
            r = sum(res[n] for n in combo) + (704 if crf else 0)
            if Fr(r, 125) > 750:
                continue
            c = 2 * (sum(cyc[n] for n in combo) + (22 if crf else 0))
            load = Fr(c, 50) / 125
            if best is None or load > best[0]:
                best = (load, combo, crf)
    print(khz, f"{float(100 * best[0]):.2f} %", best[1], 'crf', best[2])

#!/usr/bin/env python3
"""Worst packetizer load per engine over every legal mix of 1 to 16 base-format
streams per port, with and without one CRF, both ports alike, within the 75 %
class A cap (lane evidence, round 3). Formulas from mixed_stagger.py."""
import itertools
import sys
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
import mixed_stagger as m
for khz in (48, 96, 192):
    r = m.Rate(khz)
    best = {}
    for k in range(1, m.NMAX + 1):
        for crf in (True, False):
            for combo in itertools.combinations_with_replacement(m.FORMATS, k):
                res = sum(r.res[n] for n in combo) + (m.CRF_RES if crf else 0)
                if Fr(res, m.INTERVAL) > m.CAP:
                    continue
                cyc = 2 * (sum(m.build_cycles(r.ns, n) for n in combo) + (m.CRF_CYCLES if crf else 0))
                load = cyc * m.CYCLE_US / m.INTERVAL
                key = 'any' if True else None
                for kk in ('any',) + (('16',) if k == m.NMAX else ()):
                    if kk not in best or load > best[kk][0]:
                        best[kk] = (load, k, combo, crf, Fr(res, m.INTERVAL))
    for kk in ('any', '16'):
        load, k, combo, crf, bw = best[kk]
        print(f"{khz} kHz, {'any count' if kk == 'any' else 'exactly 16'}: {float(100 * load):.2f} %"
              f" with {k} streams {combo} crf {crf}, reserved {float(bw):.3f} Mb/s")

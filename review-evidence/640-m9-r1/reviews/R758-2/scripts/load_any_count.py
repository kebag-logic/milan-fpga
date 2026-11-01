"""Worst packetizer load per engine over every legal mix of 0 to 16 base-format
streams per port (both ports alike), with and without one CRF per port, within
the 75 % class A cap. Same frame, reservation and cycle formulas as the
stream-engine page (Milan v1.2 Table 4.4; 16 + NS x N cycles; CRF 22 cycles)."""
import itertools
from fractions import Fraction as Fr
FORMATS = (1, 2, 4, 6, 8)
for khz, ns in ((48, 6), (96, 12), (192, 24)):
    res = {n: 8 * (max(24 + ns * 4 * n + 1 + 22, 68) + 20) for n in FORMATS}
    cyc = {n: 16 + ns * n for n in FORMATS}
    best16 = best = None
    for k in range(1, 17):
        for crf in (True, False):
            for combo in itertools.combinations_with_replacement(FORMATS, k):
                r = sum(res[n] for n in combo) + (704 if crf else 0)
                if Fr(r, 125) > 750:
                    continue
                load = Fr(2 * (sum(cyc[n] for n in combo) + (22 if crf else 0)), 50) / 125
                if best is None or load > best[0]:
                    best = (load, k, combo, crf)
                if k == 16 and (best16 is None or load > best16[0]):
                    best16 = (load, k, combo, crf)
    print(khz, "kHz  any count:", f"{float(100 * best[0]):.2f} %", best[1], "streams", best[2], "crf", best[3])
    print(khz, "kHz  16 only  :", f"{float(100 * best16[0]):.2f} %", best16[2], "crf", best16[3])

#!/usr/bin/env python3
"""Mixed channel counts at the 32x32 stream count (16 AAF + 1 CRF per port, 48 kHz).

Tests the page's premise 'the worst case is eight channels on every stream'.
idleSlope = Milan v1.2 Table 4.4 sum over the reserved streams (34.6.1.1);
CBS per IEEE 802.1Q-2022 8.6.8.2; phases chosen by stream COUNT (3,3,3,3,2,2
in some order, the page's fewest-running rule); smaller frame first in a phase.
"""
import itertools
R = 1e9; PER = 125e-6; PH = PER / 6

def frame_bits(nch):
    return (24 * nch + 24 + 22 + 20) * 8          # no +1 octet on the wire

def bw(nch):
    return (1536 * nch + 4288) * 1e3

def worst_wait(phases, crf_phase, periods=8):
    idle = sum(bw(n) for ph in phases for n in ph) + 5632e3
    frames = []
    for p in range(periods):
        for i, ph in enumerate(phases):
            fl = ([88 * 8] if i == crf_phase else []) + sorted(frame_bits(n) for n in ph)
            frames += [(p * PER + i * PH, b, p, i) for b in fl]
    t = 0.0; c = 0.0; worst = (0.0, None)
    for ready, bits, p, i in frames:
        if t < ready:
            c = min(0.0, c + idle * (ready - t)) if c < 0 else 0.0; t = ready
        if c < 0:
            t += -c / idle; c = 0.0
        if p >= 3 and t - ready > worst[0]:
            worst = (t - ready, i)
        c += (idle - R) * bits / R; t += bits / R
    return worst[0], idle

best = (0, None)
for heavy_phase in range(6):
    for light in itertools.combinations([x for x in range(6)], 2):
        if heavy_phase in light:
            continue
        counts = [2 if i in light else 3 for i in range(6)]
        phases = [[8] * 3 if i == heavy_phase else [1] * counts[i] for i in range(6)]
        for crf in range(6):
            w, idle = worst_wait(phases, crf)
            if w > best[0]:
                best = (w, (phases, crf, idle))
w, (phases, crf, idle) = best
print("all 8-channel reference: see shaper_schedule.txt (23.925 us worst)")
print("mixed: one phase of three 8-channel streams, 13 one-channel streams elsewhere")
print("  worst shaper wait %.3f us, idleSlope %.3f Mb/s, phases %s, CRF phase %d" % (w * 1e6, idle / 1e6, phases, crf))
pk = (6 * 64 + 2 * 22) / 50e6
tot = 18.229e-6 + 0.2e-6 + pk + w + 12.336e-6 + 1e-6
print("  budget with the page's other terms: %.3f us (65 us target)" % (tot * 1e6))

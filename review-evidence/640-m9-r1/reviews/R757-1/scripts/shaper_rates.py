#!/usr/bin/env python3
"""Class A shaper wait at 32x32 (16 AAF + 1 CRF per port) at 48, 96 and 192 kHz.

Same CBS rules as shaper_schedule.py (IEEE 802.1Q-2022 8.6.8.2), Milan v1.2
Table 4.4 reservations, 8 channels per stream, phases = samples per 125 us,
fewest-first stagger, every placement of the load pattern explored by rotation
and by exhaustive search where small.
"""
import itertools

R = 1e9
PER = 125e-6

def sim(loads, crf_phase, aaf_bits, idle, nph, periods=8):
    ph_t = PER / nph
    frames = []
    for p in range(periods):
        for ph in range(nph):
            t = p * PER + ph * ph_t
            if ph == crf_phase:
                frames.append((t, 88 * 8, p))
            frames += [(t, aaf_bits, p)] * loads[ph]
    t = 0.0; credit = 0.0; worst = 0.0
    for ready, bits, p in frames:
        if t < ready:
            credit = min(0.0, credit + idle * (ready - t)) if credit < 0 else 0.0
            t = ready
        if credit < 0:
            t += -credit / idle; credit = 0.0
        start = t
        credit += (idle - R) * bits / R
        t = start + bits / R
        if p >= 3:
            worst = max(worst, start - ready)
    return worst

for rate, spp in ((48, 6), (96, 12), (192, 24)):
    nch = 8
    payload = spp * nch * 4
    aaf_bits = (payload + 24 + 22 + 20) * 8
    bw = (1536 * (rate // 48)) * nch * 1e3 + 4288e3
    idle = 16 * bw + 5632e3
    nph = spp
    print("%d kHz: frame %d octets on wire, idleSlope %.3f Mb/s (%.2f %%)" % (rate, aaf_bits // 8, idle / 1e6, idle / R * 100))
    if idle > 0.75 * R:
        print("  exceeds the 75 %% default SR class limit; the 32x32 8-channel load cannot be reserved")
        continue
    base = 16 // nph; extra = 16 % nph
    worst = (0, None)
    for heavy in itertools.combinations(range(nph), extra):
        loads = [base + (1 if i in heavy else 0) for i in range(nph)]
        for c in range(nph):
            w = sim(loads, c, aaf_bits, idle, nph)
            if w > worst[0]:
                worst = (w, (loads, c))
    print("  worst class A shaper wait over all orders: %.3f us at %s" % (worst[0] * 1e6, worst[1]))
    slot = 1 / (rate * 1e3 * 8)
    pin = 7 * slot
    pk_cycles = 4 + 5 + 6 + payload // 4 + 1
    pk = (2 * max(worst[1][0]) * pk_cycles + 2 * 22) / 50e6
    total = pin + 0.2e-6 + pk + worst[0] + 12.336e-6 + 1e-6
    print("  pin %.3f + cdc 0.200 + packetizer %.3f + shaper %.3f + interference 12.336 + MAC 1.000 = %.3f us" % (pin * 1e6, pk * 1e6, worst[0] * 1e6, total * 1e6))

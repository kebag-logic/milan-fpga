#!/usr/bin/env python3
"""Independent class-level credit-based shaper model (IEEE 802.1Q-2022 8.6.8.2).

Exact rational arithmetic. One class A queue (FIFO, frames ordered by ready time,
smaller frame first within one ready instant), one port at 1 Gb/s, optional
saturated best-effort queue whose frames (1542 octets on the wire) start whenever
the port is idle and no class A frame is eligible.

Credit rules: while a class A frame transmits, credit falls at idleSlope - R;
otherwise, while class A frames wait or credit is negative, credit rises at
idleSlope; credit above zero with an empty queue resets to zero.

Usage: cbs_model.py  (prints every figure the reviewed page derives)
"""
from fractions import Fraction as F
from itertools import permutations
import sys

R = F(10**9)                 # portTransmitRate, b/s
PERIOD = F(125, 10**6)       # class A interval
PHASE = PERIOD / 6
AAF = 258 * 8                # actual 8-channel AAF frame on the wire, bits
CRF = 88 * 8                 # Table 4.4 CRF wire size, bits
BE = (1522 + 20) * 8         # maximum interfering frame, bits
BW_AAF = F(16576 * 1000)
BW_CRF = F(5632 * 1000)


def simulate(phase_frames, idle_slope, periods=40, saturated_be=False,
             be_first=False):
    """phase_frames: list of 6 lists of frame lengths (bits) per phase.
    Returns worst wait (first-bit time minus ready time) of the last frame of
    each phase, over the final 10 periods, and whether backlog crossed a period."""
    arrivals = []
    for p in range(periods):
        for ph in range(6):
            for L in sorted(phase_frames[ph]):
                arrivals.append((p * PERIOD + ph * PHASE, L, p, ph))
    t = F(0)
    credit = F(0)
    q = []                   # waiting class A frames (ready, L, p, ph)
    i = 0
    waits = {}               # (p, ph) -> last frame wait
    carry = False
    send = idle_slope - R

    def advance(to):
        nonlocal t, credit
        dt = to - t
        if dt <= 0:
            return
        if q or credit < 0:
            credit = credit + idle_slope * dt
            if not q and credit > 0:
                credit = F(0)
        t = to

    while i < len(arrivals) or q:
        # admit arrivals at or before t
        while i < len(arrivals) and arrivals[i][0] <= t:
            q.append(arrivals[i]); i += 1
        if q and credit >= 0:
            ready, L, p, ph = q.pop(0)
            waits[(p, ph)] = max(waits.get((p, ph), F(0)), t - ready)
            dur = F(L) / R
            credit = credit + send * dur
            t = t + dur
            continue
        # nothing eligible
        if saturated_be and (i < len(arrivals) or q):
            # a best-effort frame starts now (port idle, no eligible class A)
            dur = F(BE) / R
            # class A credit evolves as if not transmitting class A
            end = t + dur
            # credit rises only while class A waits or credit negative; arrivals
            # during the BE frame make it wait
            while i < len(arrivals) and arrivals[i][0] < end:
                advance(arrivals[i][0]); q.append(arrivals[i]); i += 1
            advance(end)
            continue
        # jump to next event: credit reaching zero or next arrival
        nxt = []
        if i < len(arrivals):
            nxt.append(arrivals[i][0])
        if q and credit < 0:
            nxt.append(t + (-credit) / idle_slope)
        if not nxt:
            break
        advance(min(nxt))
    lastp = periods - 1
    worst = max(waits[(p, ph)] for p in range(periods - 10, periods)
                for ph in range(6) if (p, ph) in waits)
    per_phase = [max(waits.get((p, ph), F(0)) for p in range(periods - 10, periods))
                 for ph in range(6)]
    return worst, per_phase


def us(x):
    return float(x * 10**6)


def order_frames(loads, crf_phase, with_crf=True):
    frames = [[AAF] * n for n in loads]
    if with_crf:
        frames[crf_phase].append(CRF)
    return frames


def main():
    slope = 16 * BW_AAF + BW_CRF
    out = []
    pref = order_frames([3, 3, 2, 3, 3, 2], 2)
    w, pp = simulate(pref, slope)
    out.append(f"preferred 3,3,2,3,3,2 CRF in phase 2: worst wait {us(w):.3f} us; per phase "
               + ", ".join(f"{us(x):.3f}" for x in pp))
    w2, pp2 = simulate(pref, slope, saturated_be=True)
    out.append(f"preferred with saturated BE: worst wait {us(w2):.3f} us; per phase "
               + ", ".join(f"{us(x):.3f}" for x in pp2))
    # all orders: placements of the two light phases (15) x CRF phase (6)
    orders = set(permutations([3, 3, 3, 3, 2, 2]))
    res = []
    for o in sorted(orders):
        for c in range(6):
            w, _ = simulate(order_frames(list(o), c), slope)
            res.append((w, o, c))
    res.sort(reverse=True)
    out.append(f"orders evaluated: {len(res)}")
    for w, o, c in res[:5]:
        out.append(f"  worst-order candidates: loads {o} CRF phase {c}: {us(w):.3f} us")
    wbe, o, c = res[0]
    w3, _ = simulate(order_frames(list(o), c), slope, saturated_be=True)
    out.append(f"worst order with saturated BE: {us(w3):.3f} us")
    # without any CRF reservation on the port
    slope_nocrf = 16 * BW_AAF
    res2 = []
    for o in sorted(orders):
        w, _ = simulate(order_frames(list(o), 0, with_crf=False), slope_nocrf)
        res2.append((w, o))
    res2.sort(reverse=True)
    wp, _ = simulate(order_frames([3, 3, 2, 3, 3, 2], 0, with_crf=False), slope_nocrf)
    out.append(f"no CRF reservation, 16 AAF: preferred order {us(wp):.3f} us; worst order "
               f"{res2[0][1]} {us(res2[0][0]):.3f} us")
    # alternative load multiset {3,3,3,3,3,1}
    res3 = []
    for o in set(permutations([3, 3, 3, 3, 3, 1])):
        for c in range(6):
            w, _ = simulate(order_frames(list(o), c), slope)
            res3.append((w, o, c))
    res3.sort(reverse=True)
    out.append(f"loads 3,3,3,3,3,1 (any order, CRF anywhere): worst {us(res3[0][0]):.3f} us {res3[0][1]} CRF {res3[0][2]}")
    # fewer reservations
    for name, loads in (("two in phase 0", [2, 0, 0, 0, 0, 0]),
                        ("three in phase 0", [3, 0, 0, 0, 0, 0]),
                        ("phases 0 and 1", [1, 1, 0, 0, 0, 0]),
                        ("phases 0 and 3", [1, 0, 0, 1, 0, 0])):
        n = sum(loads)
        w, _ = simulate(order_frames(loads, 0, with_crf=False), n * BW_AAF)
        out.append(f"fewer reservations, {name}: idleSlope {float(n*BW_AAF)/1e6:.3f} Mb/s wait {us(w):.3f} us")
    # budget sums
    terms = dict(pin=F(7 * 32, 12288000), cdc=F(4, 50 * 10**6),
                 pkt=6 * F(64, 50 * 10**6) + 2 * F(22, 50 * 10**6),
                 intf=F(BE) / R, mac=F(1, 10**6))
    base = sum(terms.values())
    out.append("budget terms us: " + ", ".join(f"{k}={us(v):.3f}" for k, v in terms.items()))
    out.append(f"total with page's 18.333 = {us(base) + 18.333:.3f}; with page's 23.925 = {us(base) + 23.925:.3f}")
    out.append(f"total with model preferred = {us(base) + us(simulate(pref, slope)[0]):.3f}; with model worst = {us(base) + us(res[0][0]):.3f}")
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())

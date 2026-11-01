#!/usr/bin/env python3
"""Search start/stop reachable phase states below 16 reservations per port.

Rule and shaper from docs/design/MARK_II_STREAM_ENGINES.md at the reviewed head:
least wire time at start, spread tie order, never moved; smaller frames first;
start(k) = max(release(k), start(k-1) + L(k-1)/idleSlope). No CRF.
Usage: python3 -I probe_fewer_bound.py [walks] [steps] [seed]
"""
import random
import sys
from fractions import Fraction as Fr

FORMATS = (1, 2, 4, 6, 8)
NS_OF = {48: 6, 96: 12, 192: 24}
NMAX = 16
# Fixed terms besides the shaper wait, from the page: 48 kHz total 40.325 us;
# 96 kHz one-format row 51.293 - 18.802; 192 kHz mixed 18.093 without packetizer
# delay, 18.093 + 24.827 with its largest packetizer term.
FIXED = {48: (40.325, 40.325), 96: (32.491, 32.491), 192: (18.093, 42.920)}
PUBLISHED_16 = {48: 95.867, 96: 93.216, 192: 100.825}


def spread(P):
    if P == 6:
        return [0, 3, 1, 4, 2, 5]
    order, seen, k = [], set(), 1
    while len(order) < P:
        for j in range(k):
            p = (j * P) // k
            if p not in seen:
                seen.add(p)
                order.append(p)
        k *= 2
    return order


class Rate:
    def __init__(self, khz):
        self.khz, self.ns = khz, NS_OF[khz]
        self.P = self.ns
        self.tph = Fr(125, self.P)
        self.L = {n: 8 * (max(24 + self.ns * 4 * n + 22, 68) + 20) for n in FORMATS}
        self.res = {n: 8 * (max(24 + self.ns * 4 * n + 1 + 22, 68) + 20) for n in FORMATS}
        self.rank = {p: i for i, p in enumerate(spread(self.P))}

    def start(self, phases, n):
        best = min(range(self.P), key=lambda p: (sum(self.L[m] for m in phases[p]), self.rank[p]))
        phases[best].append(n)
        return best

    def wait(self, phases):
        slope = Fr(sum(self.res[n] for ph in phases for n in ph), 125)
        if not slope:
            return Fr(0)
        frames = []
        for p in range(self.P):
            for n in sorted(phases[p], key=lambda m: self.L[m]):
                frames.append((p * self.tph, self.L[n]))
        end, worst = None, Fr(0)
        for c in range(6):
            for rel, bits in frames:
                r = rel + c * 125
                s = r if end is None else max(r, end)
                end = s + Fr(bits) / slope
                if c >= 4:
                    worst = max(worst, s - r)
        return worst


def fmt(phases):
    return {p: sorted(ph) for p, ph in enumerate(phases) if ph}


def walk(rate, rng, steps, formats):
    phases = [[] for _ in range(rate.P)]
    best = (Fr(-1), None)
    for _ in range(steps):
        count = sum(len(ph) for ph in phases)
        if count == 0 or (count < NMAX and rng.random() < 0.55):
            rate.start(phases, rng.choice(formats))
        else:
            live = [p for p in range(rate.P) for _ in phases[p]]
            p = rng.choice(live)
            phases[p].remove(rng.choice(phases[p]))
        count = sum(len(ph) for ph in phases)
        if count < NMAX:
            w = rate.wait(phases)
            if w > best[0]:
                best = (w, [list(ph) for ph in phases])
    return best


def directed_fill_then_stop(rate, formats_fill, keep):
    """Start `formats_fill` in order, then stop every stream outside `keep` phases."""
    phases = [[] for _ in range(rate.P)]
    for n in formats_fill:
        rate.start(phases, n)
    return [list(ph) if p in keep else [] for p, ph in enumerate(phases)]


def main():
    walks = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 758
    r48 = Rate(48)
    print("calibration, 48 kHz eight-channel rows of the page")
    for label, st, want in (
        ("two in phase 0", {0: [8, 8]}, 62.259),
        ("three in phase 0", {0: [8, 8, 8]}, 83.012),
        ("two, phases 0 and 1", {0: [8], 1: [8]}, 41.425),
        ("two, phases 0 and 3", {0: [8], 3: [8]}, 0.0),
    ):
        ph = [st.get(p, []) for p in range(6)]
        print(f"  {label}: wait {float(r48.wait(ph)):.3f} page {want}")
    print()
    for khz in (48, 96, 192):
        rate = Rate(khz)
        rng = random.Random(seed + khz)
        top = (Fr(-1), None)
        for i in range(walks):
            formats = FORMATS if i % 2 else (8,)
            w, st = walk(rate, rng, steps, formats)
            if w > top[0]:
                top = (w, st)
        lo, hi = FIXED[khz]
        print(f"{khz} kHz, under 16 running, best wait over {walks} walks of {steps}: "
              f"{float(top[0]):.3f} us at {fmt(top[1])}")
        print(f"  total {float(top[0]) + lo:.3f} to {float(top[0]) + hi:.3f} us; "
              f"16-reservation published ceiling {PUBLISHED_16[khz]} us")
    r96 = Rate(96)
    st = directed_fill_then_stop(r96, [8] * 13, {0})
    print(f"\n96 kHz directed: 13 eight-channel starts, then stop all outside phase 0: {fmt(st)} "
          f"wait {float(r96.wait(st)):.3f} us, total {float(r96.wait(st)) + FIXED[96][0]:.3f} us")
    r192 = Rate(192)
    st = directed_fill_then_stop(r192, [8] * 14, {0, 1})
    print(f"192 kHz directed: 14 eight-channel starts, then stop all outside phases 0 and 1: {fmt(st)} "
          f"wait {float(r192.wait(st)):.3f} us, total {float(r192.wait(st)) + FIXED[192][0]:.3f} us "
          f"to {float(r192.wait(st)) + FIXED[192][1]:.3f} us")


if __name__ == "__main__":
    main()

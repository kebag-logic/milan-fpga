#!/usr/bin/env python3
"""Probe (lane evidence, round 4): a presentation-time step as tu clears on
both networks, against the same step on an unpaired stream. Uses
merge_model.py's Pair unchanged. Prints, per step, the packets never written
and the copies discarded as late, early, duplicate or tu, for the pair and
for one network alone.
Usage: python3 -I probe_tu_step.py <dir holding merge_model.py>"""
import random
import sys

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else ".")
import merge_model as m  # noqa: E402


def run(step, ports=(0, 1), n=4000, seed=1):
    rnd = random.Random(seed)
    drift = 150e-6
    t0 = 10_000.0 + 7.3
    lat = {0: (60, 180), 1: (1100, 1500)}
    seq0 = {0: 17, 1: 201}
    ev = []
    for j in range(n):
        tj = t0 + j * m.T * (1 + drift)
        for port in (0, 1):
            t = tj + (rnd.uniform(-m.E_X, m.E_X) if port == 1 else 0.0)
            a = tj - m.PTO + rnd.uniform(*lat[port])
            if port not in ports:
                continue
            tu = 100 <= j < 600
            if j >= 600:
                t += step
            ev.append((a, port, t, tu, (seq0[port] + j) % 256, j))
    ev.sort()
    p = m.Pair(set())
    p.trec = m.T * (1 + drift)
    for a, port, t, tu, seq, j in ev:
        p.copy(port, a, t, tu, seq, j)
    written = {pkt for (pkt, i) in p.buf.values()}
    miss = [j for j in range(n) if j not in written]
    return len(miss), (miss[0], miss[-1]) if miss else None, p.outside


def main():
    print("step_us  pair: missing, first-last, outside   primary alone: missing, first-last, outside")
    for st in (-1000, -300, -100, 100, 300, 1000):
        print(f"{st:6}   {run(st)}   {run(st, ports=(0,))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

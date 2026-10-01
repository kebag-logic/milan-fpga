#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Desk model of the revised AAF clock meter rules (#629, design round 2).

Not a model of any talker: a model of the meter's stated rules under assumed
presentation-time error shapes.

The meter sees one AAF PDU every 125 us (Milan v1.2 6.2: 6 samples per PDU at
48 kHz). It keeps one value per 16 PDUs (96 samples, 2 ms), picked where
sequence_num % 16 == 0. Two pick rules:
  first : the picked PDU's own timestamp (round 1's rule);
  mean  : the picked group's mean of (ts_i - i * 125,000 ns), i = 0..15,
          added to the group's first timestamp.
History rule (KL_crf_rx.sv:394-399): an adjacent pick spacing outside
2 ms +/- B restarts the 256-entry ring; the rate is valid after 256 fresh
intervals. Two bounds: B = 2,048 ns (KL_crf_rx.sv:290-294) and B = 4,096 ns.
The servo samples the rate once per 512 ms window (KL_mmcm_drp_servo.sv:609)
and qualifies lock on |e| < 1,024 ns (2 ppm, :232, :648); it reaches LOCKED
after 4 qualifying windows in a row (:233, :565-566). With the local clock
following exactly, e is the remote ring noise pick[k] - pick[k-256].

Error shapes, each with peak J ns per PDU timestamp:
  white : independent uniform in [-J, J];
  alt   : +J, -J alternating per PDU;
  group : +J, -J alternating per 16-PDU group (every pick of a group shares
          one sign: the shape averaging cannot remove).
J = 1,042 ns is IEEE 1722-2016 10.8 Equation 15 at 48 kHz (5 % of 20,833 ns);
1,426 ns adds KL_crf_rx's 384 ns per-timestamp quantisation for the CRF
timing points that talker followed.
Rate offset: 0 or 300 ppm of the 2 ms spacing (KL_crf_rx's 200 ppm PHC trim
plus 100 ppm oscillator margin, :280-292).

Standard library only, deterministic seed. Usage: python3 meter_rules_model.py
"""
import random

PDU_NS = 125_000
GROUP = 16
NOM_NS = PDU_NS * GROUP          # 2 ms
RING = 256
LOCK_THR = 1_024
SECONDS = 120


def picks(shape, jit, ppm, rng, rule):
    n_pdu = SECONDS * 8_000
    out = []
    acc = 0.0
    base = None
    for n in range(n_pdu):
        if shape == "white":
            e = rng.uniform(-jit, jit)
        elif shape == "alt":
            e = jit if n % 2 == 0 else -jit
        else:
            e = jit if (n // GROUP) % 2 == 0 else -jit
        ts = n * PDU_NS * (1 + ppm * 1e-6) + e
        i = n % GROUP
        if rule == "first":
            if i == 0:
                out.append(ts)
        else:
            if i == 0:
                base = ts
                acc = 0.0
            acc += ts - base - i * PDU_NS
            if i == GROUP - 1:
                out.append(base + acc / GROUP)
    return out


def grade(p, bound, ppm):
    step = NOM_NS * (1 + ppm * 1e-6)
    fresh = 0
    valid = 0
    restarts = 0
    windows = []
    for k in range(1, len(p)):
        if abs(p[k] - p[k - 1] - NOM_NS) > bound:
            restarts += 1
            fresh = 0
        else:
            fresh += 1
        ok = fresh >= RING
        valid += ok
        if k % RING == 0 and ok:
            noise = p[k] - p[k - RING] - RING * step
            windows.append(abs(noise) < LOCK_THR)
    run = 0
    lock4 = 0
    for w in windows:
        run = run + 1 if w else 0
        lock4 += run >= 4
    n = len(p) - 1
    nw = len(windows)
    return (valid / n, restarts / SECONDS,
            (sum(windows) / nw) if nw else 0.0,
            (lock4 / nw) if nw else 0.0)


def main():
    rng = random.Random(629)
    print(f"{SECONDS} s per case; bound B in ns; lock = |e| < {LOCK_THR} ns")
    print("shape  J_ns  ppm  rule   B     rate_valid  restarts/s  "
          "win<2ppm  win_in_4run")
    for shape in ("white", "alt", "group"):
        for jit in (0, 384, 1042, 1426, 2500):
            for ppm in (0, 300):
                for rule in ("first", "mean"):
                    p = picks(shape, jit, ppm, rng, rule)
                    for bound in (2_048, 4_096):
                        v, r, w, l4 = grade(p, bound, ppm)
                        print(f"{shape:5s} {jit:5d} {ppm:4d}  {rule:5s} "
                              f"{bound:5d}  {v:10.4f}  {r:10.2f}  "
                              f"{w:8.3f}  {l4:11.3f}")


if __name__ == "__main__":
    main()

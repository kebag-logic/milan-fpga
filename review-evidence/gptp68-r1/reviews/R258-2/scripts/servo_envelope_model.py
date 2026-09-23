#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer model of the #68 SERVO leg against a rate-offset master.

The controller is the documented rule in exact integers (the same shifts the
generator emits): t = (off * M) >> 6, I = clamp(I + (t >> 2), L),
trim = clamp(t - (t >> 2) + I, L), addend = -trim; a pair whose |off| exceeds
the threshold (20 us at link-up, 100 us once locked) steps by -off and writes
the bare clamped integrator. L is the parent's PHC_ADJ_MAX_C expression.

The plant is one Sync interval per pair: the master gains r ppm, and the
local PHC gains addend * clk / 8 / 2^24 ns per 125 ms interval.

It answers two questions the engine suite samples only at +-140 ppm:
  1. after a locked jump of J (|J| <= 100 us, so the first pair slews unless
     the residual offset at the jump carries it over), does the loop ever
     step on a LATER pair (a self-inflicted step), and how long does it take
     to come back inside 1 us;
  2. how the settling time grows as the master rate approaches the envelope.

Usage: servo_envelope_model.py [clk_hz]
"""

import sys

CLK = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
M = round((1 << 24) * 64 * 8 / CLK)
L = (200 * (1 << 24) * 1000 + CLK // 2) // CLK
LINKUP, LOCKED = 20_000, 100_000
NS_PER_UNIT = CLK / 8 / (1 << 24)       # ns of phase per addend unit per pair


def clamp(v, lim):
    return lim if v > lim else (-lim if v < -lim else v)


def pair(state, off_ns, linkup):
    """One consumed pair; returns (stepped, addend) and updates state."""
    off = int(round(off_ns))
    thr = LINKUP if linkup else LOCKED
    if off > thr or off < -thr:
        return True, -clamp(state["I"], L), -off
    t = (off * M) >> 6
    state["I"] = clamp(state["I"] + (t >> 2), L)
    trim = clamp(t - (t >> 2) + state["I"], L)
    return False, -trim, 0


def settle(r_ppm, jump_ns, pairs=4000):
    """Lock to a master r_ppm fast, then jump it by jump_ns while locked."""
    st = {"I": 0}
    off = 0.0
    addend = 0
    # converge first (link-up pair steps if needed), 400 pairs = 50 s
    for k in range(400):
        stepped, addend, adj = pair(st, off, k == 0)
        off += adj
        off += addend * NS_PER_UNIT - r_ppm * 125.0
    off -= jump_ns          # the master jumps ahead by jump_ns: local behind
    sign0 = 1.0 if off > 0 else -1.0
    steps_after = 0
    overshoot = 0.0
    back_in = None
    rail_pairs = 0
    for k in range(pairs):
        stepped, addend, adj = pair(st, off, False)
        if stepped and k > 0:       # the first pair is the jump itself
            steps_after += 1
        if abs(addend) == L:
            rail_pairs += 1
        overshoot = max(overshoot, -sign0 * off)
        off += adj
        off += addend * NS_PER_UNIT - r_ppm * 125.0
        if back_in is None and abs(off) < 1000.0 and not stepped:
            back_in = k + 1
    return steps_after, back_in, rail_pairs, overshoot


def main():
    print(f"clk {CLK} Hz, gain M {M}, envelope L {L} units "
          f"({L * NS_PER_UNIT / 125.0:.3f} ppm)")
    print("r_ppm  jump_us  steps_after  pairs_to_|off|<1us      s  "
          "rail_pairs  overshoot_us")
    rows = []
    for r in (-199, -190, -180, -160, -140, -100, 0, 100, 140, 160, 180,
              190, 199):
        for j in (-100_000, -90_000, -50_000, -25_000, 25_000, 50_000,
                  90_000, 100_000):
            s, b, rails, ov = settle(r, j)
            rows.append((r, j, s, b, rails, ov))
            bs = "never" if b is None else f"{b}"
            sec = "-" if b is None else f"{b * 0.125:.1f}"
            print(f"{r:5d}  {j / 1000:7.0f}  {s:11d}  {bs:>18}  {sec:>5}  "
                  f"{rails:10d}  {ov / 1000:12.1f}")
    stepped = [x for x in rows if x[2]]
    print(f"\nlocked jumps inside 100 us that later step: {len(stepped)}")
    ovr = max(rows, key=lambda x: x[5])
    print(f"largest overshoot: r={ovr[0]} ppm jump={ovr[1] / 1000:.0f} us "
          f"-> {ovr[5] / 1000:.1f} us")
    slow = max((x for x in rows if x[3] is not None), key=lambda x: x[3])
    print(f"slowest settle: r={slow[0]} ppm jump={slow[1] / 1000:.0f} us "
          f"-> {slow[3]} pairs ({slow[3] * 0.125:.1f} s)")


if __name__ == "__main__":
    main()

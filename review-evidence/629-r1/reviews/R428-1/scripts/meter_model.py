#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Desk model of the proposed AAF clock meter's decimation and history rules.

Part 1: the page picks one PDU in 96/spf "by sequence_num modulo 96/spf".
sequence_num is 8 bits and wraps at 256 (IEEE 1722-2016 4.4.4.6). For every
spf that divides 96, report the picked spacings, in samples, across the wrap.

Part 2: the page reuses KL_crf_rx's history rule unchanged: any adjacent
picked spacing outside 2 ms +/- TS_JUMP_NS restarts the ring, and the rate is
valid again only after 256 fresh intervals. TS_JUMP_NS is derived exactly as
KL_crf_rx.sv:290-294 derives it. Each picked AAF timestamp carries an
independent uniform jitter of +/-J ns and a constant rate offset. Report the
fraction of 2 ms picks at which rate_valid is high, over a long run.

Pure standard library; deterministic seed. Usage: python3 meter_model.py
"""
import math
import random

NOM_NS = 2_000_000
DRIFT = math.ceil(NOM_NS * (200 + 100) / (1_000_000 - 100))
TS_JUMP_NS = 1 << math.ceil(math.log2(DRIFT + 2 * 384))


def part1():
    print("part 1: sequence_num modulo 96/spf across the 8-bit wrap")
    for spf in [d for d in range(1, 97) if 96 % d == 0]:
        n = 96 // spf
        picks = [s for s in range(0, 256 * 3) if (s % 256) % n == 0]
        gaps = sorted({(b - a) * spf for a, b in zip(picks, picks[1:])})
        ok = gaps == [96]
        print(f"  spf={spf:2d} 96/spf={n:2d} 256%n={256 % n:2d} "
              f"picked spacings (samples)={gaps} {'uniform' if ok else 'NON-UNIFORM'}")


def part2(picks=400_000, seed=629):
    print(f"part 2: TS_JUMP_NS={TS_JUMP_NS} (KL_crf_rx derivation), "
          f"{picks} picks per case")
    rng = random.Random(seed)
    print("  jitter_ns  offset_ppm  restarts_per_s  rate_valid_fraction")
    for jit in (0, 250, 500, 750, 1000, 1250):
        for ppm in (0, 50, 100):
            step = NOM_NS * (1 + ppm * 1e-6)
            prev = rng.uniform(-jit, jit)
            fresh = 0
            valid = 0
            restarts = 0
            for k in range(1, picks):
                cur = k * step + rng.uniform(-jit, jit)
                spacing = cur - ((k - 1) * step + prev)
                prev = cur - k * step
                if abs(spacing - NOM_NS) > TS_JUMP_NS:
                    restarts += 1
                    fresh = 0
                else:
                    fresh += 1
                if fresh >= 256:
                    valid += 1
            secs = picks * NOM_NS / 1e9
            print(f"  {jit:9d}  {ppm:10d}  {restarts / secs:14.3f}  "
                  f"{valid / picks:19.4f}")


if __name__ == "__main__":
    part1()
    part2()

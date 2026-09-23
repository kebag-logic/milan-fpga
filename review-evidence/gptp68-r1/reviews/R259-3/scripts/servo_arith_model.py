#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R259-3: the SERVO leg's arithmetic, modelled on the uCPU's 64-bit
semantics (ALU ADD wraps mod 2^64; MD DIVU is a 64/32 unsigned divide with a
32-bit divisor; SAR is arithmetic), checked independently of the ROM.

(a) threshold: with RB = S_LOCK + 20000, RW = off + RB, RU = RW divu
    (2 RB + 1), the pair slews exactly when RU == 0, and that is exactly
    -T <= off <= T for T = 20000 (S_LOCK 0) and T = 100000 (S_LOCK 80000);
(b) e_sat(reg, lim) equals clamp(reg, -lim, lim) for every reg the leg can
    feed it, and the retired integrator clamp of the base equals e_sat there;
(c) every divisor fits the DIVU's 32-bit divisor field;
(d) the slew arm's MULS operand (off, 32 bits signed) is exact for |off| <=
    100 us, and the pre-clamp PI output stays far from e_sat's wrap bound at
    every clock the generator is used with.
"""

from __future__ import annotations

import random
import sys

M64 = (1 << 64) - 1
FAILS = 0


def u64(x: int) -> int:
    return x & M64


def s64(x: int) -> int:
    x &= M64
    return x - (1 << 64) if x >> 63 else x


def sar(x: int, n: int) -> int:
    return s64(x) >> n


def check(cond: bool, msg: str) -> None:
    global FAILS
    if not cond:
        FAILS += 1
        print(f"FAIL {msg}")


def servo_slews(off: int, s_lock: int) -> bool:
    rb = u64(s_lock + 20000)
    rw = u64(off + rb)
    rb = u64(rb + rb)
    rb = u64(rb + 1)
    assert rb < (1 << 32)
    return (rw // (rb & 0xFFFFFFFF)) == 0


def e_sat(reg: int, lim: int) -> int:
    rw = u64(reg + lim)
    ru = rw // (2 * lim + 1)
    if ru == 0:
        return s64(reg)
    s = sar(rw, 63) & M64
    r = u64(lim ^ s)
    return s64(r - s)


def base_iclamp(i: int, ilim: int) -> int:
    rb = u64(i + ilim)
    if (rb >> 32) == 0 and (rb & 0xFFFFFFFF) < 2 * ilim + 1:
        return s64(i)
    return -ilim if (u64(i) >> 63) == 1 else ilim


def ppm_addend(ppm: int, clk: int) -> int:
    return (ppm * (1 << 24) * 1000 + clk // 2) // clk


def main() -> int:
    rnd = random.Random(68)
    # (a) threshold, exhaustive near both thresholds and random elsewhere
    n = 0
    for s_lock, t in ((0, 20000), (80000, 100000)):
        edge = list(range(-t - 3000, -t + 3000)) + list(range(t - 3000, t + 3000))
        edge += [0, 1, -1, (1 << 63) - 1, -(1 << 63), (1 << 63) - 1 - t,
                 (1 << 63) - t, -(1 << 63) + t, 2 ** 32, -(2 ** 32), 2 ** 31, -(2 ** 31)]
        rand = [rnd.randrange(-(1 << 63), 1 << 63) for _ in range(200000)]
        rand += [rnd.randrange(-4 * t, 4 * t) for _ in range(200000)]
        for off in edge + rand:
            n += 1
            check(servo_slews(off, s_lock) == (-t <= off <= t),
                  f"threshold T={t} off={off}")
    print(f"(a) threshold decision == (-T <= off <= T): {n} offsets, T in 20 us / 100 us")
    # (b) e_sat and the base integrator clamp
    n = 0
    for clk in (2_000_000, 25_000_000, 50_000_000, 100_000_000, 125_000_000):
        lim = ppm_addend(200, clk)
        vals = list(range(-lim - 2000, -lim + 2000)) + list(range(lim - 2000, lim + 2000))
        vals += [rnd.randrange(-(1 << 62), 1 << 62) for _ in range(100000)]
        vals += [(1 << 63) - 1 - lim, -(1 << 63)]
        for v in vals:
            n += 1
            want = max(-lim, min(lim, v))
            check(e_sat(v, lim) == want, f"e_sat clk={clk} v={v}")
            if -(1 << 62) <= v < (1 << 62):
                check(base_iclamp(v, lim) == e_sat(v, lim), f"base clamp clk={clk} v={v}")
        print(f"(b) clk {clk:>9}: lim {lim}; e_sat == clamp and == base integrator clamp")
        # (c) divisors
        check(2 * lim + 1 < (1 << 32), "e_sat divisor fits 32 bits")
    check(2 * 100000 + 1 < (1 << 32) and 2 * 20000 + 1 < (1 << 32), "threshold divisors")
    print("(c) every DIVU divisor fits the 32-bit divisor field")
    # (d) MULS operand and PI range
    for clk in (2_000_000, 25_000_000, 50_000_000, 100_000_000, 125_000_000):
        gain = round((1 << 24) * 64 * 8 / clk)
        lim = ppm_addend(200, clk)
        worst = 0
        for off in (100000, -100000):
            check(-(1 << 31) <= off < (1 << 31), "MULS operand is 32-bit exact")
            t = (off * gain) >> 6
            i = max(-lim, min(lim, lim * (1 if off > 0 else -1) + (t >> 2)))
            pi = (t - (t >> 2)) + i
            worst = max(worst, abs(pi))
        check(worst < (1 << 62), "PI output far from the e_sat wrap bound")
        print(f"(d) clk {clk:>9}: gain {gain}, worst |PI| at 100 us {worst} "
              f"({worst / lim:.2f} x the envelope), clamped to {lim}")
    print(f"\n{FAILS} failure(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

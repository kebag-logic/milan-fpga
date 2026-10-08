#!/usr/bin/env python3
"""R548-2: exhaustive model of KL_maap's reset seed and LFSR step.

Checks over every value of the 16-bit MAC fold f = mac[15:0] ^ mac[31:16]
(every station MAC maps to one f): the new seed is never zero; it equals the
round-1 seed for every f that did not give zero; the step
{r[14:0], r15^r14^r12^r3} has a single cycle of length 65535 through every
nonzero state (so no nonzero seed reaches zero); and the probe/announce
draws 518+r[5:0] / 30488+r[9:0] stay inside 518..581 / 30488..31511.
"""


def step(r: int) -> int:
    b = ((r >> 15) ^ (r >> 14) ^ (r >> 12) ^ (r >> 3)) & 1
    return ((r << 1) & 0xFFFF) | b


def main() -> int:
    ok = True
    for f in range(1 << 16):
        old = 0xACE1 ^ f
        new = 0xACE1 if old == 0 else old
        if new == 0 or (old != 0 and new != old):
            ok = False
    print(f"seed nonzero for all 65536 folds, unchanged where old != 0: {ok}")
    r, n, seen_zero = 0xACE1, 0, False
    pmin = amin = 1 << 30
    pmax = amax = 0
    while True:
        r = step(r)
        n += 1
        seen_zero |= r == 0
        p, a = 518 + (r & 0x3F), 30488 + (r & 0x3FF)
        pmin, pmax, amin, amax = min(pmin, p), max(pmax, p), min(amin, a), max(amax, a)
        if r == 0xACE1 or n > 70000:
            break
    print(f"period from 0xACE1: {n} (maximal 65535: {n == 65535}); zero reached: {seen_zero}")
    print(f"probe draw ms {pmin}..{pmax}; announce draw ms {amin}..{amax}")
    print(f"step(0) == 0 (fixed point): {step(0) == 0}")
    ok = ok and n == 65535 and not seen_zero and (pmin, pmax) == (518, 581) \
        and (amin, amax) == (30488, 31511)
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

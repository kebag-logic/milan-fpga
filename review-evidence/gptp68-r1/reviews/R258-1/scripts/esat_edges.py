#!/usr/bin/env python3
"""Exact 64-bit model of the head generator's e_sat sequence (ALU ADD imm,
DIVU by 2*lim+1, CMP Q against zero, SAR 63 of the SUM, MOVE lim, XOR, SUB),
checked against the documented contract "saturate the signed value to
[-lim, +lim]" at the edges of the 64-bit range. Prints every input whose
result breaks the contract. Usage: esat_edges.py"""
M64 = (1 << 64) - 1


def s64(x: int) -> int:
    """Two's-complement view of a 64-bit word."""
    x &= M64
    return x - (1 << 64) if x >> 63 else x


def e_sat(reg: int, lim: int) -> int:
    """The emitted sequence, word for word."""
    rw = (reg + lim) & M64
    ru = rw // (2 * lim + 1)            # DIVU: 64/32 unsigned quotient
    if ru == 0:
        return s64(reg)
    s = -1 if rw >> 63 else 0           # SAR 63 of the sum
    return s64(((lim ^ (s & M64)) - s) & M64)


def main() -> None:
    """Report contract violations near both ends of the range."""
    for lim in (20000, 1677722, 26844):
        viol = []
        probes = list(range(-(1 << 63), -(1 << 63) + 3 * lim)) [::997] + \
            list(range((1 << 63) - 3 * lim, 1 << 63))[::997] + \
            [(1 << 63) - 1, (1 << 63) - lim, (1 << 63) - lim - 1, -(1 << 63),
             lim, lim + 1, -lim, -lim - 1, 0]
        for r in probes:
            want = max(-lim, min(lim, r))
            got = e_sat(r, lim)
            if got != want:
                viol.append((r, got, want))
        first = viol[0] if viol else None
        lo = min(v[0] for v in viol) if viol else None
        print(f"lim {lim}: {len(viol)} of {len(probes)} probes violate; "
              f"lowest violating input {lo}; example {first}")
    print(f"window: inputs above 2^63-1-lim wrap the sum negative; "
          f"2^63-1 = {(1 << 63) - 1}")


if __name__ == "__main__":
    main()

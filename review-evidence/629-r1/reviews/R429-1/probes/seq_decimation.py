#!/usr/bin/env python3
"""Disposable review probe (R429-1): the design's AAF meter picks one PDU in
D = 96/spf "by sequence_num modulo 96/spf". sequence_num is 8 bits and wraps
at 256 (IEEE 1722-2016 4.4.4.6). For each spf that divides 96, report whether
the picked PDUs stay 96 samples apart across the wrap, and the spacing that
appears at the wrap otherwise (in samples; the meter's jump rule is 2 ms,
96 samples, +/-2048 ns, i.e. well under one sample)."""
for spf in sorted(d for d in range(1, 97) if 96 % d == 0):
    D = 96 // spf
    picks = [n for n in range(3 * 256) if (n % 256) % D == 0]  # absolute PDU index
    gaps = sorted({(b - a) * spf for a, b in zip(picks, picks[1:])})
    ok = gaps == [96]
    print(f"spf={spf:3d} D=96/spf={D:3d} 256%D={256 % D:3d} "
          f"picked spacings (samples)={gaps} {'OK' if ok else 'BROKEN at wrap'}")

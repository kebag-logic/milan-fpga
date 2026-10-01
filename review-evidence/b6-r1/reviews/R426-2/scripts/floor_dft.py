#!/usr/bin/env python3
"""Independent floor check: 48,000-point DFT of the regenerated tone loop
(8 x S32_LE, 24-bit in bits 31:8), band 20 Hz to 20 kHz, THD+N (all band bins
but the fundamental) and SNR (also excluding harmonics below 20 kHz); plus the
analytic floor of a -1 dBFS tone over uniform 24-bit rounding in that band.
Usage: floor_dft.py <loop.bin>"""
import math, sys
import numpy as np
x = np.fromfile(sys.argv[1], dtype="<i4").reshape(-1, 8) >> 8
N = len(x); assert N == 48000
for ch, f0 in ((0, 997), (1, 9973)):
    X = np.fft.rfft(x[:, ch].astype(np.float64))
    P = np.abs(X) ** 2
    # mask the excluded bins; subtracting them from a sum the fundamental dominates
    # loses the residual to float64 rounding
    m = np.zeros(len(P), dtype=bool); m[20:20001] = True; m[f0] = False
    fund = P[f0]
    rest = P[m].sum()
    for k in range(2, 20000 // f0 + 1):
        m[k * f0] = False
    nh = P[m].sum()
    print(f"ch{ch} {f0} Hz: THD+N {10*math.log10(rest/fund):.4f} dB, SNR {10*math.log10(fund/nh):.4f} dB, "
          f"peak {np.abs(x[:, ch]).max()}, other channels zero {bool((x[:, 2:] == 0).all())}")
A = 2 ** 23 * 10 ** (-1 / 20)
noise = (1 / 12) * (19980 / 24000)
print(f"analytic: -1 dBFS amplitude {A:.1f}; THD+N floor {10*math.log10(noise/(A*A/2)):.3f} dB")

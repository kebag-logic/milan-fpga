#!/usr/bin/env python3
"""Independent floor check of the B6 tone loop, without the grading tool.

Usage: floor_dft.py <tone-loop.bin>   (48,000 frames, 8 x S32_LE, 24-bit in bits 31:8)

The loop is exactly periodic over 48,000 frames, so a 48,000-point DFT has 1 Hz
bins and no leakage. THD+N = in-band (20 Hz..20 kHz) power other than the
fundamental bin, over the fundamental. SNR also removes harmonic bins below
20 kHz. The analytic figure is uniform 24-bit rounding noise (q^2/12, q = 2^-23
of full scale) in the band's share of 0..24 kHz, against a -1 dBFS sine.
A 3 dB band error is planted (the band power doubled) to show it would be seen.
"""
import sys
import numpy as np

raw = np.fromfile(sys.argv[1], dtype="<i4")
assert raw.size == 48000 * 8, raw.size
x = raw.reshape(48000, 8).astype(np.float64) / 2.0**31
N = 48000
for ch, f0 in ((0, 997), (1, 9973)):
    X = np.fft.rfft(x[:, ch])
    P = np.abs(X) ** 2
    band = np.arange(20, 20001)
    fund = P[f0]
    keep = band[band != f0]  # mask the fundamental; subtracting it would cancel catastrophically
    resid = P[keep].sum()
    harm = [k * f0 for k in range(2, 200) if k * f0 <= 20000]
    noise = P[np.setdiff1d(keep, harm)].sum()
    thdn = 10 * np.log10(resid / fund)
    snr = 10 * np.log10(fund / noise)
    A = np.sqrt(fund) / (N / 2)
    q = 2.0 ** -23
    analytic = 10 * np.log10((q * q / 12) * ((20000 - 20) / 24000) / (A * A / 2))
    planted = 10 * np.log10(2 * resid / fund)
    print(f"ch{ch} {f0} Hz: amplitude {20*np.log10(A):.4f} dBFS; DFT THD+N {thdn:.4f} dB; DFT SNR {snr:.4f} dB; "
          f"analytic floor {analytic:.4f} dB; planted 3 dB band error -> {planted:.4f} dB; "
          f"harmonic bins {len(harm)}; nonzero channels 2..7: {int(np.count_nonzero(x[:, 2:]))}")

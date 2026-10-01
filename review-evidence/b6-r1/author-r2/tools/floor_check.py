#!/usr/bin/env python3
"""Independent check of lane B6's published 24-bit floor (read-only).

usage: floor_check.py <dir holding b6_tone.py> <controls.json>

Does not use b6_thdn.py. The loop is exactly periodic over 48,000 frames, so a 48,000-point
DFT has 1 Hz bins and no leakage:
  THD+N = every bin from 20 Hz to 20 kHz but the fundamental, over the fundamental;
  SNR   = the same band without the harmonics below 20 kHz, fundamental over it;
  analytic: a sine of amplitude A over rounding noise of variance 1/12 LSB^2 spread evenly
  over 0 to 24 kHz, of which (20,000 - 20) / 24,000 falls in the band.
A 3 dB error in the band computation moves the floor by 3.01 dB, against agreement here in
the hundredths.
"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import b6_tone as T  # noqa: E402

pub = json.load(open(sys.argv[2]))["floor"]
FS, N = T.FS, T.N
lp = T.loop().astype(np.float64)
A = T.AMP
snr_an = 10 * np.log10((A * A / 2) / ((1 / 12) * (20000 - 20) / (FS / 2)))
print(f"analytic 24-bit rounding floor, amplitude {A:.1f} LSB, 20 Hz to 20 kHz: SNR {snr_an:.3f} dB, "
      f"THD+N {-snr_an:.3f} dB")
worst = 0.0
for ch, f in ((0, T.F0), (1, T.F1)):
    X = np.fft.rfft(lp[:, ch])
    P = np.abs(X) ** 2
    # sum the band with the excluded bins masked out, never by subtraction from a sum the
    # fundamental dominates (that loses the residual to float64 rounding)
    band = np.zeros(len(P), dtype=bool)
    band[20:20001] = True
    band[f] = False
    fund = P[f]
    resid = P[band].sum()
    for h in range(2, 20000 // f + 1):
        band[h * f] = False
    resid_h = P[band].sum()
    thdn = 10 * np.log10(resid / fund)
    snr = 10 * np.log10(fund / resid_h)
    d_t = thdn - pub[ch]["thdn_db"]
    d_s = snr - pub[ch]["snr_db"]
    worst = max(worst, abs(d_t), abs(d_s))
    print(f"{f} Hz: DFT THD+N {thdn:.3f} dB, SNR {snr:.3f} dB; published THD+N {pub[ch]['thdn_db']:.3f} dB, "
          f"SNR {pub[ch]['snr_db']:.3f} dB; difference {d_t:+.4f} / {d_s:+.4f} dB; against analytic "
          f"{thdn + snr_an:+.3f} dB")
print(f"largest difference from the published floor {worst:.4f} dB; a 3 dB band error would show as 3.01 dB")
sys.exit(0 if worst < 0.05 else 1)

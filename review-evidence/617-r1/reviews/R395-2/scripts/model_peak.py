#!/usr/bin/env python3
"""Unpulled acquisition-transient peak of the bound aligner (same integer PI as
model_guard.py), per clock and source offset: engagement mid-sample, err0 = 0."""
import sys
def peak(clk, r, frames=200000):
    PN = clk / 48000.0; ULIM = 3200; ACCLIM = ULIM << 12
    phi = PN / 2; ref = int(phi); acc = 0; u = 0; lo = hi = phi
    Pf = PN * (1 - r * 1e-6)
    for _ in range(frames):
        phi += Pf - PN * (1 - u * 1e-6 / 16)
        lo = min(lo, phi); hi = max(hi, phi)
        err = int(phi // 1) - ref
        u = max(-ULIM, min(ULIM, -(err << 2) - (acc >> 12)))
        acc = max(-ACCLIM, min(ACCLIM, acc + err))
    return ref - lo, hi - ref
for clk in (50e6, 100e6):
    for r in (-50, -10.64, 50):
        d, u = peak(clk, r)
        print(f"clk {clk/1e6:.0f} MHz  source {r:+7.2f} ppm: transient peak {max(d, u):7.2f} cycles")

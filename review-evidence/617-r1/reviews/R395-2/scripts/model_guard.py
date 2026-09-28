#!/usr/bin/env python3
"""Frame-level model of KL_media_grid_align as bound in milan_datapath at 377d1ac3.

Integer PI exactly as the RTL (u = clamp(-(err<<2) - (acc>>>12)), acc += err,
both clamped), keep-off pull of the engagement capture into [K, DIV-K], NCO
period shortened by u/16 ppm. phi = close position in cycles after the delayed
tick (tst). The walk's crossing is the wrap of phi (phi < 0 or phi >= P).
Reports, per source offset r (ppm, TDM frame rate relative to the NCO nominal),
the worst excursion of phi toward the crossing after engagement, over every
engagement capture tst0 in [0, P).
Usage: model_guard.py [clk_hz] [keepoff]   (defaults 50e6, 256)
"""
import sys
import numpy as np

CLK = float(sys.argv[1]) if len(sys.argv) > 1 else 50e6
K = int(sys.argv[2]) if len(sys.argv) > 2 else None
FS = 48000.0
PN = CLK / FS
DIV = int(CLK // FS)
if K is None:
    K = min(DIV // 4, 256)
HI = DIV - K
ULIM = 3200
ACCLIM = ULIM << 12
FRAMES = 150000

rates = np.array([r for r in range(-100, 101, 5)] + [-10.64, 10.64], dtype=float)
# engagement capture phases: every integer tst0, plus a 0.5-cycle offset set
tst0 = np.arange(0, int(np.floor(PN)) + 1, dtype=float)
tst0 = np.concatenate([tst0 + 0.0, tst0 + 0.5])
tst0 = tst0[tst0 < PN]
R, T0 = np.meshgrid(rates, tst0, indexing="ij")
R = R.ravel(); T0 = T0.ravel()
ref = np.clip(np.floor(T0), K, HI).astype(np.int64)
phi = T0.copy()
acc = np.zeros_like(ref)
u = np.zeros_like(ref)
Pf = PN * (1.0 - R * 1e-6)           # frame period
lo = phi.copy(); hi = phi.copy()      # extremes after engagement
lo_after = np.full_like(phi, np.inf); hi_after = np.full_like(phi, -np.inf)
crossed = np.zeros(phi.shape, dtype=bool)
for n in range(FRAMES):
    Pt = PN * (1.0 - u * (1e-6 / 16.0))
    phi = phi + Pf - Pt
    crossed |= (phi < 0) | (phi >= PN)
    lo = np.minimum(lo, phi); hi = np.maximum(hi, phi)
    if n >= 64:
        lo_after = np.minimum(lo_after, phi); hi_after = np.maximum(hi_after, phi)
    err = np.floor(phi).astype(np.int64) - ref
    unew = -(err << 2) - (acc >> 12)
    u = np.clip(unew, -ULIM, ULIM)
    acc = np.clip(acc + err, -ACCLIM, ACCLIM)

print(f"clk={CLK:.0f} P={PN:.4f} DIV={DIV} keepoff={K} frames={FRAMES}")
print("rate_ppm  min_phi_all  max_phi_all  margin_all  min_phi>=64  max_phi>=64  margin>=64  any_cross  worst_tst0")
for r in rates:
    m = R == r
    marg_all = np.minimum(lo[m], PN - hi[m])
    marg64 = np.minimum(lo_after[m], PN - hi_after[m])
    i = np.argmin(marg_all)
    print(f"{r:8.2f}  {lo[m].min():11.2f}  {hi[m].max():11.2f}  {marg_all.min():10.2f}  "
          f"{lo_after[m].min():11.2f}  {hi_after[m].max():11.2f}  {marg64.min():10.2f}  "
          f"{int(crossed[m].sum()):9d}  {T0[m][i]:8.1f}")
# the transient peak for an unpulled engagement at mid-sample, per rate
print("unpulled transient peak |phi - tst0| (tst0 = P/2):")
for r in rates:
    m = (R == r) & (np.abs(T0 - np.floor(PN / 2)) < 0.01)
    print(f"  {r:8.2f} ppm: down {float(T0[m][0] - lo[m][0]):7.2f}  up {float(hi[m][0] - T0[m][0]):7.2f}")

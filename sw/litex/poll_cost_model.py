#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Project the pointer-writeback's CPU-side pps/bandwidth gain from silicon-measured data.

The RTL sim (test_ring_writeback.py) shows the ENGINE does ~400 kpps / 4.8 Gbit/s and the
writeback costs +2.4% — so the datapath is not the limit. The limit is CPU-side: every
NAPI poll does an MMIO wr_ptr(+dropped) CSR read that stalls the in-order VexiiRiscv. This
model extracts that cost from the measured rx-usecs-low sweep and projects the ceiling with
the CSR read replaced by a cached shadow read (~0 cost).

Measured on silicon 2026-07-05 (single TCP flow, MTU 1500, VexiiRiscv @100 MHz):
"""
# idle-poll period L (us)  ->  RX Mbit/s  (down-sweep + up-sweep, averaged where overlapping)
SWEEP = [(5, 5.06), (20, 7.34), (50, 15.3), (200, 27.9),
         (500, 32.3), (1000, 36.1), (2000, 35.9), (4000, 37.0)]
MTU_BYTES = 1500

def pps(mbit):
    return mbit * 1e6 / 8 / MTU_BYTES

print(__doc__)
print(f"  {'L(us)':>6} {'RX Mbit':>8} {'RX kpps':>8}")
for L, m in SWEEP:
    print(f"  {L:6d} {m:8.1f} {pps(m)/1e3:8.2f}")

# --- model: throughput lost to empty-poll CSR reads during idle gaps -------------------
# During a flow the poll re-arms every L us after an empty poll; each empty poll costs the
# CPU c_us on MMIO CSR stalls. Effective throughput T(L) = Tmax * (1 - min(1, c_us/L))**g,
# with g>1 capturing the near-degenerate collapse when polling saturates the core. Fit the
# two well-separated anchors (L=4000 ~ CSR-free, and the steep knee) then report Tmax.
import math
# solve on a small grid (no scipy dependency)
best = None
for Tmax in [x/10 for x in range(360, 700)]:          # 36.0 .. 70.0
    for c10 in range(5, 400):                          # c_us 0.5 .. 40
        c = c10/10
        for g10 in range(10, 60):                       # g 1.0 .. 6.0
            g = g10/10
            err = 0.0
            for L, m in SWEEP:
                frac = min(0.999, c/L)
                pred = Tmax * (1-frac)**g
                err += (pred-m)**2
            if best is None or err < best[0]:
                best = (err, Tmax, c, g)
_, Tmax, c, g = best
print(f"\nfit: Tmax={Tmax:.1f} Mbit/s  c_empty_poll={c:.1f} us  g={g:.1f}  (rms={math.sqrt(best[0]/len(SWEEP)):.1f})")

print("\n--- projection: writeback replaces the MMIO CSR read with a cached shadow read ---")
print("The cached read costs ~0.05 us vs the fitted ~%.1f us MMIO stall, so c_empty_poll -> ~0" % c)
print("=> the driver can poll at LOW latency (e.g. L=20us) WITHOUT the collapse:")
for L in (20, 50, 200):
    cur = Tmax*(1-min(0.999, c/L))**g
    wb  = Tmax*(1-min(0.999, 0.05/L))**g
    print(f"   L={L:4d}us:  now {cur:5.1f} Mbit/s ({pps(cur)/1e3:5.1f} kpps)  ->"
          f"  writeback {wb:5.1f} Mbit/s ({pps(wb)/1e3:5.1f} kpps)")

print(f"\nSingle-flow ceiling with CSR cost removed ~= Tmax = {Tmax:.0f} Mbit/s "
      f"({pps(Tmax)/1e3:.1f} kpps).")
print("HONEST READ: writeback recovers the single-flow plateau at LOW latency (removes the")
print("latency<->throughput tradeoff), but a single flow stays ~Tmax — bounded by per-packet")
print("CPU cost, not CSR reads. The large headroom (engine 400 kpps) is realised only by")
print("AGGREGATE / many-flow load (the switch control plane), where per-poll CSR cost caps pps.")

#!/usr/bin/env python3
"""R484-1 receipt: recompute #656's rates from the RTL and harness constants.

Inputs (cited by path at head d0e29f6d):
  axis clock          50 MHz            tb/verilator/nvm_capture_cpu/recipe.py CPU_HZ
  audio clock model   +782 twice per axis cycle, toggle at >= 1591
                                        tb/verilator/milan_dp/sim_ax1x1gptp.cpp:321-343
  TDM frame           SLOTS*WORD_BITS*2*BCLK_HALF = 8*32*2*1 = 512 clk_tdm cycles
                                        hdl/milan/milan_datapath.sv:902-908 (defaults :151,:152,:162)
  old talker period   kHz*6/48000 axis cycles      (parent c0280fc0, sim_ax1x1gptp.cpp)
  new talker period   6*512 audio rising edges     (head, sim_ax1x1gptp.cpp:89,500-505)
  verify_abort pin    20 ms window holds exactly 160 RX PDUs
                                        tb/verilator/milan_dp_gptp/verify_abort.py:68

The talker model replays Harness::schedule()/clocks() exactly for an idle
RX path (no PTP reservation inside the window, which holds for the no-TX
control's "initial payload" window: Sync is queued within 1500 cycles of
configure(), next Sync at +125 ms, first Pdelay at 1.2 s).
"""
from fractions import Fraction as F

HZ = 50_000_000
fsync = F(HZ) * 782 / 1591 / 512
ppm = (fsync / 48000 - 1) * 10**6
excess = 48000 - fsync                       # events/s per pair, axis-paced talker
print(f"audio clock        = {float(F(HZ) * 782 / 1591):.3f} Hz")
print(f"TDM FSYNC          = {float(fsync):.6f} Hz  ({float(ppm):+.4f} ppm vs 48 kHz)")
print(f"old talker excess  = {float(excess):.6f} events/s per pair")
print(f"slip period        = {float(1 / excess):.6f} s  (exact {1 / excess})")
print(f"per 10 ppm at 48k  = {48000 * 10e-6:.3f} events/s")
pdu = F(3072 * 1591, 782)
print(f"new PDU period     = {float(pdu):.6f} axis cycles = 6250 + {pdu - 6250}")
print(f"new PDU rate       = {float(HZ / pdu):.6f} /s; samples {float(6 * HZ / pdu):.6f} /s"
      f" (equals FSYNC: {6 * HZ / pdu == fsync})")
W = HZ // 50
print(f"20 ms window       = {W} cycles = {float(W / pdu):.6f} PDUs; "
      f"deficit {float(160 * pdu - W):.4f} cycles; nominal 159-fraction {float((160 * pdu - W) / pdu) * 100:.4f} %")

# Exact replay of the harness clock and talker for one full pattern period.
PERIOD_PDUS = 391                            # lcm(3072, 782) / 3072
PERIOD_CYC = 391 * 3072 * 1591 // 782        # 2,443,776 axis cycles
def edges_after_each_tick(n, acc0=0, lvl0=0):
    acc, lvl, edges, out = acc0, lvl0, 0, []
    for _ in range(n):
        for _half in range(2):               # quarters 0 and 4
            acc += 782
            if acc >= 1591:
                acc -= 1591
                lvl ^= 1
                if lvl:
                    edges += 1
        out.append(edges)
    return out

N = 3 * PERIOD_CYC + W + 10
E = edges_after_each_tick(N)
def fire_cycles(anchor_cycle):
    """schedule() at the start of tick c sees E[c-1]; anchor = configure()."""
    nxt = E[anchor_cycle - 1]
    fires = []
    for c in range(anchor_cycle, N):
        if E[c - 1] >= nxt:
            fires.append(c)
            nxt += 3072
    return fires

def window_count_histogram(fires, lo, hi):
    import bisect
    hist = {}
    for s in range(lo, hi):
        k = bisect.bisect_left(fires, s + W) - bisect.bisect_left(fires, s)
        hist[k] = hist.get(k, 0) + 1
    return hist

worst = None
for anchor in (1000, 1001, 1777, 2500):      # several configure() phases of the edge pattern
    f = fire_cycles(anchor)
    gaps = sorted({b - a for a, b in zip(f, f[1:])})
    h = window_count_histogram(f, anchor + 10_000, anchor + 10_000 + PERIOD_CYC)
    tot = sum(h.values())
    print(f"anchor {anchor}: inter-PDU gaps {gaps}; window counts "
          + ", ".join(f"{k}: {v} ({100 * v / tot:.4f} %)" for k, v in sorted(h.items())))
    worst = h

# Old pacing: a strict 6250-cycle lattice from configure().
old = list(range(1000, N, 6250))
h = window_count_histogram(old, 20_000, 20_000 + 6250 * 10)
print(f"old pacing: window counts {h} (phase-invariant: {list(h) == [160]})")

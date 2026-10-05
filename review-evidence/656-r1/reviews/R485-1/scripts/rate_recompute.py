#!/usr/bin/env python3
"""Recompute the #656 slip rate and period from RTL and harness constants.

Sources (exact head d0e29f6d):
  sim_ax1x1gptp.cpp:325-329  audio clock: +782 per half axis cycle, toggle at
                             1591, rising edge every other toggle -> 782/1591
                             rising edges per axis cycle
  sim_ax1x1gptp.cpp:765      FSYNC period 512 audio edges (checked in-harness)
  sim_ax1x1gptp.cpp:89       new pacing: 6 * 512 audio edges per PDU
  c0280fc0 sim_ax1x1gptp.cpp old pacing: kHz * 6 / 48000 axis cycles per PDU
  Makefile CLOCK_RECIPE      kHz = 50 MHz (CPU_HZ)
  milan_datapath.sv:5905     mga_sel_w = int_clk_selected_r | follow_sel_r:
                             PI aligner holds media_tick_p on FSYNC at INTERNAL
  milan_datapath.sv:1302     KL_chan_map_capture.tick_i = media_tick_p (pop)
  KL_media_nco.sv:150,163    servo trim u in 1/16 ppm
"""
from fractions import Fraction as F

HZ = 50_000_000
audio = F(HZ) * 782 / 1591                    # rising edges per second
fsync = audio / 512                           # TDM frame rate = drain rate under A2-a
old_pdu_cyc = F(HZ * 6, 48000)                # old peer pacing
new_pdu_cyc = F(6 * 512) * 1591 / 782         # new peer pacing, axis cycles
old_rate = F(HZ) / old_pdu_cyc * 6            # samples/s pushed (old)
new_rate = F(HZ) / new_pdu_cyc * 6            # samples/s pushed (new)
ppm = (old_rate / fsync - 1) * 10**6
excess = old_rate - fsync
print(f"audio clock            = {float(audio):.6f} Hz")
print(f"FSYNC (drain, A2-a)    = {float(fsync):.6f} Hz ({float((fsync / 48000 - 1) * 1e6):+.4f} ppm vs 48 kHz)")
print(f"old PDU period         = {old_pdu_cyc} axis cycles -> {float(old_rate):.6f} samples/s")
print(f"new PDU period         = {new_pdu_cyc} = {float(new_pdu_cyc):.6f} axis cycles "
      f"(6250 + {new_pdu_cyc - 6250}) -> {float(new_rate):.6f} samples/s")
print(f"old talker vs grid     = {float(ppm):+.4f} ppm faster")
print(f"queue over-fill        = {float(excess):.6f} events/s per pair")
print(f"slip period            = {float(1 / excess):.6f} s")
print(f"new talker vs grid     = {float(new_rate - fsync)} events/s (exact)")
print(f"servo trim for plan    = {float((fsync / 48000 - 1) * 1e6 * 16):.2f} LSB of 1/16 ppm (trace: -170)")
print(f"slip rate per 10 ppm   = {48000 * 10e-6:.3f} events/s (per ppm {48000e-6:.4f})")
L = F(HZ, 50)                                  # 20 ms window
print(f"20 ms window / new PDU = {float(L / new_pdu_cyc):.6f} PDUs; 159-count band = "
      f"{float(160 * new_pdu_cyc - L):.4f} cycles = {float((160 * new_pdu_cyc - L) / new_pdu_cyc) * 100:.4f} % of phases")
print(f"trace gap check        = 4.513547 -> 6.471693 s: {6.471693 - 4.513547:.6f} s")

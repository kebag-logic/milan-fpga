#!/usr/bin/env python3
"""Round-2 re-derivations of the stream-engine and area-plan figures.

Usage: python3 -I arith_check.py   (no inputs; every constant names its source)
"""
from fractions import Fraction as F
def r(x, n=3): return round(float(x), n)
out = []
# Save path: N25Q128 Table 32 maxima (tPP 5 ms), 12.5 MHz single lane.
xfer = F((1 + 3 + 256) * 8, 12_500_000) * 1000          # ms
t_page = xfer + F(11, 1000) + 5 + xfer
out.append(f"t_page {r(t_page)} ms (page {r(xfer)} + 0.011 + 5.000 + read-back {r(xfer)})")
T = 10 + F(535, 100) + 2 * 1 + 32 * F(535, 100) + 32 * F(535, 100)
out.append(f"T_worst {r(T,2)} ms; margin {r(500-T,2)} ms ({r((500-T)/5,2)} %)")
# Render buffer: Milan v1.2 4.4.2.1 2.126 ms; design keeps 2.25 ms.
for k, fs in ((1, 48000), (2, 96000), (4, 192000)):
    need = F(225, 100000) * fs; depth = 128 * k
    bits = 8 * depth * 32
    out.append(f"{fs} Hz: 2.25 ms = {r(need,1)} samples, depth {depth} = {r(F(depth,fs)*1000)} ms, {bits} bits = {bits/32768} RAMB36")
# 75 % class A cap at 192 kHz: Table 4.4 W = 96N + 67 octets, x 64 kb/s.
bw = lambda n: (96 * n + 67) * 64     # kb/s
out.append(f"192k: 16x8ch+CRF {16*bw(8)+5632} kb/s; 13x8ch+CRF {13*bw(8)+5632}; 14x8ch+CRF {14*bw(8)+5632} (cap 750000)")
out.append(f"192k mix 13x8+1x4+2x1 {13*bw(8)+bw(4)+2*bw(1)} kb/s, +CRF {13*bw(8)+bw(4)+2*bw(1)+5632}")
# Engine load: 16 + NS*N cycles per frame, CRF 22; 6250 cycles per 125 us at 50 MHz; both ports.
for ns, mix, crf in ((6, [8]*16, 1), (12, [8]*16, 1), (24, [8]*13 + [4] + [1, 1], 0)):
    cyc = 2 * (sum(16 + ns * n for n in mix) + 22 * crf)
    out.append(f"NS {ns}: engine load {r(F(cyc, 6250)*100, 2)} %")
# Fixed terms and totals.
pin48, pin96 = F(7, 8) * F(10**6, 48000), F(7, 8) * F(10**6, 96000)
fx48 = pin48 + F(2, 10) + F(2 * (192 + 22) * 20, 1000) + F(12336, 1000) + 1
fx96 = pin96 + F(2, 10) + F(2 * (224 + 22) * 20, 1000) + F(12336, 1000) + 1
out.append(f"fixed 48k {r(fx48)}; 96k {r(fx96)}")
out.append(f"48k one format {r(F(23106,1000)+fx48)}; mixed bound {r(F(55542,1000)+fx48)}; reached {r(F(53085,1000)+pin48+F(2,10)+F(768,100)+F(12336,1000)+1)}")
out.append(f"96k one format {r(F(18802,1000)+fx96)}; mixed bound {r(F(60725,1000)+fx96)}; reached {r(F(43215,1000)+pin96+F(2,10)+F(896,100)+F(12336,1000)+1)}")
# Witness: phase 0 three 8ch, phase 1 five 2ch, eight 1ch elsewhere, no CRF (48 kHz, Table 4.4).
slope = 3 * 16576 + 5 * 7360 + 8 * 5824                  # kb/s
wait = F(3 * 2064 + 4 * 912, slope) * 1000 - F(10**6, 48000)
out.append(f"witness idleSlope {slope} kb/s; phase-1 last frame wait {r(wait)} us")
out.append(f"three co-phased 8ch alone: wait {r(F(2*2064, 3*16576)*1000)} us; with all fixed terms {r(F(2*2064, 3*16576)*1000 + fx48)} us")
# Max wire time per 48 kHz phase under the least-wire-time rule, 16 streams (argument in REPORT).
out.append("phase cap 48k: 2 x 2064 + 2064 = 6192 bits -> 3 x 64 = 192 cycles, packetizer term 2 x (192 + 22) x 20 ns = 8.560 us")
# Area plan.
out.append(f"area central {r(20.7+0.25+1.75+1.0-1.75-0.5,2)}k low {r(19.1+0.25+1.25+0.5-2.5-0.8,2)}k high {r(22.4+0.25+2.25+1.75-1.0-0.2,2)}k")
fab = [0.5, 1.0, 0.5, 4.0, 2.0, 2.0, 4.0, 6.0, 1.0, 0.5, 1.0, 4.5]
out.append(f"BRAM fabric {sum(fab)}; total {sum(fab)+113.0-11.5+16.0}; over {sum(fab)+113.0-11.5+16.0-121.5}")
out.append(f"shipping 52008 / 63400 = {r(F(52008,63400)*100,2)} %")
print("\n".join(out))

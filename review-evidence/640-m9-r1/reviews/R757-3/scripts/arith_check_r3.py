#!/usr/bin/env python3
"""Re-derive the round-3 figures of the stream-engine page.

Usage: python3 -I arith_check_r3.py
Each line prints the derived value next to the page's figure.
"""
p = 5.35e-3                                    # t_page used, s
t_page = (1 + 3 + 256) * 8 / 12.5e6 * 2 + 0.011e-3 + 5.0e-3
print(f"t_page {t_page * 1e3:.4f} ms (page: 5.344 ms, used as 5.35 ms)")
T = (10 + 5.35 + 2 * 1 + 32 * 5.35 + 32 * 5.35)
print(f"T_worst {T:.2f} ms (page: 359.75 ms); margin {500 - T:.2f} ms")
# S2 token bucket: 0.9 t / p - 33 >= 273 + 0.1 t / p  ->  t >= 306 p / 0.8
t_done = 306 * p / 0.8
print(f"compaction done by {t_done:.4f} s = {306 / 0.8:.1f} p (page: 382.5 p, 2.046 s)")
A = 32 + 0.1 * (306 / 0.8)
print(f"replay pages A <= {A:.2f} (page: 70.25, so 70); work <= {240 + int(A) + 1} (page: 311)")
free = 1024 - 311
need = free - 392
t_next = (need - 32) * p / 0.1
print(f"free after {free}; next trigger needs {need} pages; t >= {t_next:.3f} s (page: 15.46 s)")
spare = 0.9 * t_next - 32 * p - need * 1e-3
print(f"erase time available {spare:.2f} s against 12 s (page: 13.42 s)")
# engine load at 192 kHz
c8, c4, c1 = 16 + 24 * 8, 16 + 24 * 4, 16 + 24 * 1
print(f"192 kHz load 14 x 8ch: {2 * 14 * 8000 * c8 / 50e6 * 100:.3f} % (page: 93.18 %); "
      f"reserved {14 * 53.440:.3f} Mb/s (page: 748.160)")
print(f"192 kHz load at 16: {2 * 8000 * (13 * c8 + c4 + 2 * c1) / 50e6 * 100:.3f} % (page: 92.67 %)")
print(f"16 co-ready frames: 15 x 2064 / 270.848 Mb/s = {15 * 2064 / 270.848:.2f} us (page: about 114 us)")
for w in (62.259, 83.012, 41.425, 0.000):
    print(f"fewer reservations total {w:.3f} + 40.325 = {w + 40.325:.3f} us")
print(f"192 kHz mixed: 57.905 + 24.827 + 18.093 = {57.905 + 24.827 + 18.093:.3f} us (page: 100.825)")
print(f"192 kHz fixed: 4.557 + 0.200 + 1.000 + 12.336 = {4.557 + 0.2 + 1.0 + 12.336:.3f} us (page: 18.093)")
print(f"48 kHz packetizer: 2 x (6192 x 64 / 2064 + 22) x 20 ns = {2 * (6192 * 64 / 2064 + 22) * 0.02:.3f} us (page: 8.560)")
print(f"96 kHz packetizer: 2 x (7200 x 112 / 3600 + 22) x 20 ns = {2 * (7200 * 112 / 3600 + 22) * 0.02:.3f} us (page: 9.840)")
print(f"E_x as written: 2 + 2 x 125 x 200e-6 + 4 x 0.040 = {2 + 2 * 125 * 200e-6 + 0.16:.3f} us (page: 2.210)")
print(f"merge map: 2.667 ms / 125 us = {2666.667 / 125:.2f} packets -> bits 0..21; drift over 22 packets at 200 ppm {22 * 125 * 200e-6:.3f} us")

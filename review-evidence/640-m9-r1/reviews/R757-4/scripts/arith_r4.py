#!/usr/bin/env python3
"""Reviewer's arithmetic for the round-4 figures. Usage: python3 -I arith_r4.py"""
p = 5.35
print("T_worst", round(10 + p + 2 + 32 * p + 32 * p, 3), "ms; with a zeroing page", round(10 + p + 2 + 32 * p + 32 * p + p, 3), "ms; bound 500 ms")
sep = 125 + 2792
drift = 200e-6 * sep
print("latch to latch", sep, "us; drift", round(drift, 4), "us; E_x", round(2.0 + 0.584 + 0.160, 3), "us (unrounded", round(2.0 + drift + 0.160, 4), ")")
print("A4 at 2.667 ms span plus 125 us:", round(2666.667 + 125, 3), "us; at the 2 ms default the arrival bound is", 2125, "us, E_x", round(2 + 200e-6 * (125 + 2125) + 0.16, 3))
print("class A transit 2 ms leaves", round(2792 - 2000, 1), "us for the talker's stamp to wire; worst stated talker bound 123.337 us")
print("drift across 22 packets at 200 ppm", round(22 * 125 * 200e-6, 3), "us; window margin", round(62.5 - 2.744 - 0.55, 3), "us; neighbour separation", round(125 - 0.55 - 2.744, 3), "us")
print("span in packets", round(2666.667 / 125, 2), "so a lapse takes at most 22 packets =", 22 * 0.125, "ms")
print("sweep 32 contexts x 31.25 ms =", 32 * 31.25, "ms")
# a restart after a failed header, read under S1 and S2, from a trigger at 392 pages free
comp = 2.046
erase = (12 + 0.32) / 0.9
t = comp + erase + comp
print(f"failed header at the end of a compaction: {comp} s + standby erase {erase:.2f} s + second compaction {comp} s = {t:.2f} s; "
      f"appended pages under S2 <= {32 + 0.1 * t / (p / 1000):.0f}, against 392 free")
t2 = comp + erase + comp + erase + comp
print(f"a second failed header in a row: {t2:.2f} s; appended pages <= {32 + 0.1 * t2 / (p / 1000):.0f}, against 392 free")

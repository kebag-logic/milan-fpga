"""Section 14's gPTP assumption, recomputed from its own table (SPLIT_CONTROL_MEMORY.md, gPTP's share).

Usage: python3 -I gptp_arith.py
Frames 46/s and servo runs 16/s at 40,000 CPU cycles each (20,000 to 100,000), CPU 100 MHz.
"""
HZ, CYC, FRAMES, SERVO, WIN = 100e6, 40_000, 46, 16, 0.087
unit_ms = CYC / HZ * 1e3
print(f"load {100 * (FRAMES + SERVO) * CYC / HZ:.2f} % (range {100 * 62 * 20_000 / HZ:.2f} to {100 * 62 * 100_000 / HZ:.2f})")
print(f"frames in {WIN * 1e3:.0f} ms at the average rate: {FRAMES * WIN:.2f} -> doc's row add {4 * unit_ms:.2f} ms")
print(f"frames and servo runs in that window: {(FRAMES + SERVO) * WIN:.2f} -> {(FRAMES + SERVO) * WIN * unit_ms:.2f} ms")
print(f"one Sync and Follow_Up on each port plus their two servo runs: 6 units -> {6 * unit_ms:.2f} ms")
print(f"8x8/2if last SRP record 15.96 ms + 1.6 = {15.96 + 1.6:.2f}; + 2.4 = {15.96 + 2.4:.2f} against 18")
print(f"pass: doc 0.8 ms (two records); with one servo run {3 * unit_ms:.1f} ms")
for name, p in (("S", 3.7186), ("U", 4 * 1.9664)):
    print(f"{name}: pass {p + 0.8:.2f} (doc) / {p + 1.2:.2f}; Pdelay two passes {2 * (p + 0.8):.2f} / {2 * (p + 1.2):.2f} vs 15")

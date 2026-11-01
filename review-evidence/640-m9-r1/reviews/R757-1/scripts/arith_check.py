#!/usr/bin/env python3
"""Re-derive the save path, Block RAM ledger and LUT arithmetic of PR #828."""
MHZ = 12.5e6
xfer = (1 + 3 + 256) * 8 / MHZ * 1e3                  # ms, program command and read-back each
t_page = xfer + 0.011 + 5.0 + xfer
print("t_page %.4f ms (page shows 5.343, used 5.35)" % t_page)
T = 10 + 1 + 32 * 5.35 + 32 * 5.35
print("T_worst as written %.1f ms, margin %.1f ms (%.1f %%)" % (T, 500 - T, (500 - T) / 5))
T2 = 10 + 2 * 1 + 5.35 + 32 * 5.35 + 32 * 5.35
print("with a compaction page in flight and a second erase suspend: %.2f ms" % T2)
print("pages/s at maxima %.1f; 10 %% of that %.0f B/s" % (1000 / 5.35, 0.1 * 1000 / 5.35 * 256))
print("compaction 240 pages %.3f s; erase 4 x tSE %d s; boot read 256 KiB %.1f ms" % (240 * 5.35e-3, 4 * 3, 256 * 1024 * 8 / MHZ * 1e3))
print("907 names, ~100 names per 32-page save: %.3f s" % (907 / 100 * 32 * 5.35e-3))
rom = 98056 + 62 * 985; sram = 57152 + 62 * 3951
print("firmware 64 streams: rom %d sram %d total %d B = %.1f RAMB36" % (rom, sram, rom + sram, (rom + sram) / 4096))
stage = 3344 + 62 * (13264 - 3344) / 14
print("stage %.0f B = %.2f RAMB36" % (stage, stage / 4096))
fabric = [0.5, 1.0, 0.5, 1.0, 2.0, 2.0, 4.0, 6.0, 1.0, 0.5, 1.0, 4.5]
print("fabric subtotal %.1f, total %.1f vs usable 121.5" % (sum(fabric), sum(fabric) + 113 - 11.5 + 16))
print("names from flash: %.2f tiles" % (907 * 64 / 4096))
base = 52008 - 24354 - 481 + 3948 + 3102
print("split estimate %d" % base)
lo = base - (3900 + 1500 + 1500 + 2000 + 1000 + 5200); hi = base - (3200 + 400 + 500 + 1500 + 1000 + 5200)
print("owner levers range %d to %d" % (lo, hi))
print("32x32 central %.2fk, range %.2fk to %.2fk" % (20.7 + 1.75 + 1.0 - 1.75 - 0.5, lo / 1e3 + 1.25 + 0.5 - 2.5 - 0.8, hi / 1e3 + 2.25 + 1.75 - 1.0 - 0.2))
print("lever 6 net of the retained timestamp return: %d LUT (page credits ~5.2k)" % (5194 - 218 - 32))
print("datapath difference row %d" % (43425 - (24354 + 481 + 5194 + 3014 + 1281 + 3289 + 2204 + 506 + 1066)))
print("crossbar rows %d, diagnostics %d" % (835 + 143 + 77 + 499 + 368 + 627 + 265 + 475, 671 + 285 + 721 + 527))
for rate in (48, 96, 192):
    need = 2.25e-3 * rate * 1e3
    print("render buffer at %d kHz: 2.25 ms needs %.0f samples; 128-sample depth covers %.3f ms" % (rate, need, 128 / (rate * 1e3) * 1e3))

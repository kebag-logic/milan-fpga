"""Recompute every derived figure PR #835 adds to docs/design/MARK_II_AREA_PLAN.md.

Inputs are the measured rows the page cites (basis rows; #665 issuecomment-6569635407;
the owner's ranges in #640 issuecomment-6545523624 and middles in issuecomment-6545540394).
Each line prints PASS or FAIL; exits 1 on any FAIL. No repository file is read.
"""
import math
import sys

fails = 0


def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}: got {got}, page says {want}")


# Measured inputs
BASIS, PP, MAAP, SPLIT_CPU, MBX, SOC_CPU = 52_008, 24_354, 481, 3_948, 3_102, 3_249
owner_start = BASIS - PP - MAAP + SPLIT_CPU + MBX
check("owner chain", owner_start, 34_223)
start = owner_start - SOC_CPU
check("start, CPU counted once", start, 30_974)
check("one CPU net change", SPLIT_CPU - SOC_CPU, 699)
check("start via net change", BASIS - PP - MAAP + (SPLIT_CPU - SOC_CPU) + MBX, 30_974)

# Owner middles (issuecomment-6545540394), lever 4 now 0
mid = {1: 1_000, 2: 1_000, 3: 1_750, 4: 0, 5: 1_000, 6: 5_200}
running, totals = start, {}
for k in range(1, 7):
    running -= mid[k]
    totals[k] = running
check("after levers 1-3", totals[3], 27_224)
check("after lever 4", totals[4], 27_224)
check("owner chain after lever 4 crediting 3,249", owner_start - 3_750 - SOC_CPU, 27_224)
check("owner middle 3.55k overstatement, rounded to 0.1k", round((3_550 - SOC_CPU) / 1000, 1), 0.3)
page_running = {1: 30.0, 2: 29.0, 3: 27.2, 4: 27.2, 5: 26.2, 6: 21.0}
for k in range(1, 7):
    check(f"running total lever {k} (k, 1 dp)", round(totals[k] / 1000, 1), page_running[k])

# Owner ranges (issuecomment-6545523624), mapped to the 16:40 order; lever 4 contributes 0
ranges = {"ddr3": (400, 1_500), "bus": (500, 1_500), "csr": (1_500, 2_000), "mmcm": (1_000, 1_000),
          "gptp": (5_200, 5_200)}
lo = start - sum(r[1] for r in ranges.values())
hi = start - sum(r[0] for r in ranges.values())
check("six levers low (k, 1 dp)", round(lo / 1000, 1), 19.8)
check("six levers high (k, 1 dp)", round(hi / 1000, 1), 22.4)

# 32x32 table (k): central, low, high
rows = [(0.25, 0.25, 0.25), (1.75, 1.25, 2.25), (1.0, 0.5, 1.75), (-1.75, -2.5, -1.0), (-0.5, -0.8, -0.2)]
central = 21.0 + sum(r[0] for r in rows)
low = 19.8 + sum(r[1] for r in rows)
high = 22.4 + sum(r[2] for r in rows)
check("32x32 central", round(central, 2), 21.75)
check("32x32 low", round(low, 2), 18.5)
check("32x32 high", round(high, 2), 25.45)
check("central miss of the 20,000 ceiling (k)", round(central - 20.0, 2), 1.75)
check("32x32 central from the exact 21,024 (k, nearest 0.05)", round(round((totals[6] + 750) / 50) * 50 / 1000, 2), 21.75)

# Console UART
char_us = 10 / 115_200 * 1e6
check("character time us (3 dp)", round(char_us, 3), 86.806)
check("16 characters ms (3 dp)", round(16 * char_us / 1000, 3), 1.389)
check("23 character times ms (3 dp)", round(23 * char_us / 1000, 3), 1.997)
check("24 character times ms (3 dp)", round(24 * char_us / 1000, 3), 2.083)
completions = math.floor(2_000 / char_us) + 1  # completions inside a 2.0 ms gap, first at its start
check("characters completing within 2.0 ms", completions, 24)
check("next power of two >= 24", 1 << (completions - 1).bit_length(), 32)
check("32 characters ms (3 dp)", round(32 * char_us / 1000, 3), 2.778)
check("per-pass share ms", 18 / 9, 2.0)

print("FAILURES", fails)
sys.exit(1 if fails else 0)

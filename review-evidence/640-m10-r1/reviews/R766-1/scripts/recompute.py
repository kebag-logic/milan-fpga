"""Recompute every derived figure the PR #835 delta states, from its cited inputs,
and check each stated value appears verbatim on docs/design/MARK_II_AREA_PLAN.md.

Usage: python3 -I recompute.py <clone>   (exit 0 when every check holds)
"""
import math
import sys
from pathlib import Path

page = (Path(sys.argv[1]) / "docs/design/MARK_II_AREA_PLAN.md").read_text(encoding="utf-8")
fails = 0


def check(label, ok, stated):
    global fails
    present = stated is None or stated in page
    status = "PASS" if ok and present else "FAIL"
    if status == "FAIL":
        fails += 1
    print(f"{status} {label}" + ("" if stated is None else f" | page text {stated!r} present={present}"))


# Inputs: basis rows and the owner's chain (measured rows, #640 issuecomment-6545523624).
basis, pp, maap, split_cpu, mbx, soc_cpu = 52008, 24354, 481, 3948, 3102, 3249
owner_start = basis - pp - maap + split_cpu + mbx
check(f"owner chain 34,223 = {owner_start}", owner_start == 34223, "=34,223 the owner's 34.2k")
start = owner_start - soc_cpu
check(f"start once-counted 30,974 = {start}", start == 30974, "=30,974 about 31.0k LUTs")
check(f"net CPU change +699 = {split_cpu - soc_cpu}", split_cpu - soc_cpu == 699, "| +699 |")
l123 = start - 1000 - 1000 - 1750
check(f"after levers 1-3 27,224 = {l123}", l123 == 27224, "| After levers 1 to 3, central | 27,224 |")
owner_after4 = owner_start - 3750 - soc_cpu
check(f"owner chain after lever 4 crediting 3,249 = {owner_after4}", owner_after4 == 27224,
      "34,223 - 3,750 - 3,249")
check(f"owner middle 3.55k overstates 3,249 by {3550 - soc_cpu}", round((3550 - soc_cpu) / 1000, 1) == 0.3,
      "overstated that by 0.3k")

# Running totals (lever 4 = 0).
run, totals = start, []
for saving in (1000, 1000, 1750, 0, 1000, 5200):
    run -= saving
    totals.append(run)
stated = ["~30.0k", "~29.0k", "~27.2k", "~27.2k", "~26.2k", "~21.0k"]
for t, s in zip(totals, stated):
    check(f"running total {t} -> {s}", f"~{t / 1000:.1f}k" == s, f"| {s} |")

# Ranges, owner's per-lever ranges (#640 issuecomment-6545523624), lever 4 at 0.
best = start - (1500 + 1500 + 2000 + 1000 + 5200)
worst = start - (400 + 500 + 1500 + 1000 + 5200)
check(f"1x1 range {best}..{worst} -> 19.8k to 22.4k",
      (round(best / 1000, 1), round(worst / 1000, 1)) == (19.8, 22.4), "The ranges then give 19.8k to 22.4k")
old_best = owner_start - (3900 + 1500 + 1500 + 2000 + 1000 + 5200)
old_worst = owner_start - (3200 + 400 + 500 + 1500 + 1000 + 5200)
check(f"old range {old_best}..{old_worst} was 19.1k to 22.4k (dev text)",
      (round(old_best / 1000, 1), round(old_worst / 1000, 1)) == (19.1, 22.4), None)

# 32x32 sums.
c = 21.0 + 0.25 + 1.75 + 1.0 - 1.75 - 0.5
lo = 19.8 + 0.25 + 1.25 + 0.5 - 2.5 - 0.8
hi = 22.4 + 0.25 + 2.25 + 1.75 - 1.0 - 0.2
check(f"32x32 central {c:.2f}", math.isclose(c, 21.75), "**~21.75k**")
check(f"32x32 range {lo:.2f}..{hi:.2f}", math.isclose(lo, 18.5) and math.isclose(hi, 25.45), "**18.5k to 25.45k**")
check(f"ceiling miss {c - 20:.2f}", math.isclose(c - 20, 1.75), "misses the ceiling by about 1.75k")

# Console UART.
tau_us = 10 / 115200 * 1e6
check(f"character time {tau_us:.3f} us", f"{tau_us:.3f}" == "86.806", "86.806 µs")
check(f"16-char fill {16 * tau_us / 1000:.3f} ms", f"{16 * tau_us / 1000:.3f}" == "1.389", "1.389 ms")
n_in_gap = math.floor(2000 / tau_us) + 1  # completions in any 2.0 ms window
check(f"chars completing in a 2.0 ms gap = {n_in_gap}", n_in_gap == 24, "| 24 |")
check(f"23 x tau = {23 * tau_us / 1000:.3f} ms, 24 x tau = {24 * tau_us / 1000:.3f} ms",
      f"{23 * tau_us / 1000:.3f}" == "1.997" and f"{24 * tau_us / 1000:.3f}" == "2.083",
      "23 character times are 1.997 ms; 24 are 2.083 ms")
buf = 1 << (n_in_gap - 1).bit_length()
check(f"next power of two >= 24 is {buf}", buf == 32, "32 bytes, the next power of two")
check(f"32 x tau = {32 * tau_us / 1000:.3f} ms", f"{32 * tau_us / 1000:.3f}" == "2.778", "2.778 ms")
check("share 18 ms / 9 passes = 2.0 ms", 18 / 9 == 2.0, "18 ms / 9 passes")

print(f"RESULT: {'PASS' if fails == 0 else 'FAIL'} ({fails} failure(s))")
sys.exit(1 if fails else 0)

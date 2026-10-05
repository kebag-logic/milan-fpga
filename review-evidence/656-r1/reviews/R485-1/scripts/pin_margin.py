#!/usr/bin/env python3
"""Measure the 160-PDU no-TX window's phase margin from a probe transcript.

Input: a transcript with 'PROBE done cyc=N' (each RX AAF completion) and
'PROBE window start=S end=E' lines. For each window, report the count of
completions in [S, E), the slack before the first and after the last, and the
smallest uniform shift of the window (earlier or later) that would change the
count, i.e. the phase margin of the exact-160 pin.
"""
import re
import sys

text = open(sys.argv[1]).read()
done = [int(x) for x in re.findall(r"PROBE done cyc=(\d+)", text)]
for s, e in re.findall(r"PROBE window start=(\d+) end=(\d+)", text):
    s, e = int(s), int(e)
    inside = [c for c in done if s <= c < e]
    before = [c for c in done if c < s]
    after = [c for c in done if c >= e]
    first, last = inside[0], inside[-1]
    gaps = [b - a for a, b in zip(inside, inside[1:])]
    # later shift d: loses first when s+d > first, gains next when e+d > after[0]
    lose_late = first - s + 1
    gain_late = after[0] - e + 1 if after else None
    # earlier shift d: loses last when e-d <= last, gains prev when s-d <= before[-1]
    lose_early = e - last
    gain_early = s - before[-1] if before else None
    print(f"window [{s},{e}) count={len(inside)} first-start={first - s} end-last={e - last} "
          f"next-end={after[0] - e if after else 'n/a'} start-prev={s - before[-1] if before else 'n/a'} "
          f"gap_min={min(gaps)} gap_max={max(gaps)} mean_gap={(last - first) / (len(inside) - 1):.4f}")
    late = "count drops" if gain_late is None or lose_late < gain_late else "count rises"
    early = "count drops" if gain_early is None or lose_early < gain_early else "count rises"
    print(f"  later shift: first change after {min(lose_late, gain_late or 10**9)} cycles ({late}); "
          f"earlier shift: first change after {min(lose_early, gain_early or 10**9)} cycles ({early})")

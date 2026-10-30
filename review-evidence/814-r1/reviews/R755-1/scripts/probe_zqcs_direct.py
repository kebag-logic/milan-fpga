#!/usr/bin/env python3
"""Reviewer probe: ZQCS commands on the DFI, LiteDRAM's refresher against the shipping one.

Usage: probe_zqcs_direct.py <repo-root> [zqcs_period_cycles]

Runs the gate's own DramSoC (board DDR3 part, 100 MHz, idle) with the ZQCS
period shortened from int(100e6/1 Hz) to Z cycles (default 10). With tREFI 782,
gcd(Z, tREFI) is 2 for both Z = 10 and Z = 100,000,000, and Z - 1 is odd for
both, so a ZQCS can coincide with a refresh's end on an idle controller exactly
when the sequencer-done offset k is even, at either period. Counts the PRECHARGE,
REFRESH and ZQCS commands each refresher puts on the DFI.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
Z = int(sys.argv[2]) if len(sys.argv) > 2 else 10
sys.path.insert(0, str(root / "sw" / "litex"))

from litedram.core.refresher import Refresher  # noqa: E402
import milan_soc  # noqa: E402
import test_soc_timing_cuts as gate  # noqa: E402

shipping = milan_soc.RegisteredRefresher


def plain(settings, clk_freq, zqcs_freq=1e0, postponing=1):
    return Refresher(settings, clk_freq, zqcs_freq=clk_freq / Z, postponing=postponing)


def staged(settings, clk_freq, zqcs_freq=1e0, postponing=1):
    return shipping(settings, clk_freq, zqcs_freq=clk_freq / Z, postponing=postponing)


CYCLES = 782 * 6 + 400
out = {}
for label, cls in (("LiteDRAM Refresher", plain), ("RegisteredRefresher (shipping)", staged)):
    seen = gate.dfi_commands(cls, CYCLES)
    counts = {}
    for _, _, name, _ in seen:
        counts[name] = counts.get(name, 0) + 1
    zq = [cycle for cycle, _, name, _ in seen if name == "ZQCS"]
    out[label] = counts
    print(f"{label}: ZQCS period {Z} cycles, {CYCLES} idle cycles: {counts}; ZQCS at {zq}")
print("RESULT: measured")

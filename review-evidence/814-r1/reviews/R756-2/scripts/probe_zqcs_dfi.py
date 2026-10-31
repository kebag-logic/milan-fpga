#!/usr/bin/env python3
"""Probe: ZQCS commands on the DFI, staged versus LiteDRAM's own refresher.

The ZQCS period is shortened (ControllerSettings.refresh_zqcs_freq) to a value
of the same parity class as the shipping one (gcd with tREFI = 2, as for
100 MHz / 1 Hz), so the coincidence LiteDRAM needs can be seen in a short run.
Everything else is the test's DramSoC: the shipping add_staged_sdram call at
100 MHz on MT41J256M16 1:4.

Usage: python3 probe_zqcs_dfi.py <repo>/sw/litex <zqcs_period_cycles> <cycles>
"""
import math
import sys

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402
import litedram.core.controller as ctl  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402

PERIOD, CYCLES = int(sys.argv[2]), int(sys.argv[3])
Original = ctl.ControllerSettings


class ShortZQ(Original):
    def __init__(self, **kwargs):
        kwargs.setdefault("refresh_zqcs_freq", t.SYS_HZ / PERIOD)
        Original.__init__(self, **kwargs)


ctl.ControllerSettings = ShortZQ
print(f"zqcs period {PERIOD} cycles, gcd with tREFI 782 = {math.gcd(782, PERIOD)}")
for label, stage in (("staged", None), ("plain", Refresher)):
    cmds = t.dfi_commands(stage, CYCLES)
    zq = [c for c in cmds if c[2] == "ZQCS"]
    ref = [c for c in cmds if c[2] == "REFRESH"]
    print(f"{label}: REFRESH {len(ref)} at {[c[0] for c in ref][:6]}; ZQCS {len(zq)} at {[c[0] for c in zq][:6]}")
print("RESULT: DONE")

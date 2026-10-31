#!/usr/bin/env python3
"""Probe: every idle DFI command of one refresher over a long run, as JSON.

Uses the test's own DramSoC and dfi_commands (the shipping add_staged_sdram call at
100 MHz on MT41J256M16 1:4), with LiteDRAM's ZQCS period cut to <period> sys cycles
through ControllerSettings.refresh_zqcs_freq, and the refresher class one of:
  staged      the shipping milan_soc.RegisteredRefresher
  plain       LiteDRAM's own Refresher
  undelayed   the test's UndelayedZQCSRefresher (registered request, no ZQCS hold)
Also prints the controller's tREFI, tRP, tRFC and tZQCS in sys cycles.

Usage: python3 probe_zqcs_equiv.py <repo>/sw/litex <period> <cycles> <stage> <out.json>
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402
import litedram.core.controller as ctl  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402

PERIOD, CYCLES, STAGE, OUT = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
Original = ctl.ControllerSettings


class ShortZQ(Original):
    def __init__(self, **kwargs):
        kwargs.setdefault("refresh_zqcs_freq", t.SYS_HZ / PERIOD)
        Original.__init__(self, **kwargs)


ctl.ControllerSettings = ShortZQ
stage = {"staged": None, "plain": Refresher, "undelayed": t.UndelayedZQCSRefresher}[STAGE]
soc = t.build(t.DramSoC, stage=stage, name="RegisteredRefresher")
timing = soc.sdram.controller.settings.timing
print(f"timing cycles: tREFI {timing.tREFI} tRP {timing.tRP} tRFC {timing.tRFC} tZQCS {timing.tZQCS}; "
      f"zqcs period {int(t.SYS_HZ / (t.SYS_HZ / PERIOD))}")
cmds = t.dfi_commands(stage, CYCLES)
with open(OUT, "w") as fh:
    json.dump(cmds, fh)
zq = [c[0] for c in cmds if c[2] == "ZQCS"]
ref = [c[0] for c in cmds if c[2] == "REFRESH"]
print(f"{STAGE} period {PERIOD}: {len(cmds)} commands, REFRESH {len(ref)}, ZQCS {len(zq)} at {zq}")
print("RESULT: DONE")

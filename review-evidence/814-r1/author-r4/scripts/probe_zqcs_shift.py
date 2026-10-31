#!/usr/bin/env python3
"""probe_zqcs_shift.py <repo>/sw/litex <period> <cycles>: DFI commands of the shipping
RegisteredRefresher, LiteDRAM's Refresher and the stage without the ZQCS delay, with the
ZQCS period shortened to <period> sys cycles. Prints each, and whether shipping == plain + 1."""
import math
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
import test_soc_timing_cuts as t  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402
from litex.soc.interconnect import stream  # noqa: E402
from migen import Module  # noqa: E402

PERIOD, CYCLES = int(sys.argv[2]), int(sys.argv[3])


def short(cls):
    class Short(cls):
        def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
            cls.__init__(self, settings, clk_freq, zqcs_freq=clk_freq / PERIOD, postponing=postponing)
    return Short


class Undelayed(Module):
    def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
        self.submodules.refresher = r = Refresher(settings, clk_freq, zqcs_freq=zqcs_freq, postponing=postponing)
        self.cmd = cmd = stream.Endpoint(r.cmd.description)
        self.sync += [cmd.valid.eq(r.cmd.valid), cmd.last.eq(r.cmd.last)]
        self.comb += [r.cmd.connect(cmd, omit={"valid", "last", "ready"}), r.cmd.ready.eq(cmd.ready)]


print(f"zqcs period {PERIOD}, gcd with tREFI 782 = {math.gcd(782, PERIOD)}, {CYCLES} cycles")
runs = {}
for label, cls in (("shipping", milan_soc.RegisteredRefresher), ("plain", Refresher), ("undelayed", Undelayed)):
    cmds = t.dfi_commands(short(cls), CYCLES)
    runs[label] = cmds
    for kind in ("PRECHARGE", "REFRESH", "ZQCS"):
        at = [c[0] for c in cmds if c[2] == kind]
        print(f"{label}: {kind} {len(at)} at {at[:8]}")
shifted = [(c + 1, i, n, a) for c, i, n, a in runs["plain"] if c + 1 < CYCLES]
for label in ("shipping", "undelayed"):
    print(f"{label} == plain + 1: {runs[label] == shifted}")

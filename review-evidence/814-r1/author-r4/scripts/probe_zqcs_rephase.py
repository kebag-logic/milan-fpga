#!/usr/bin/env python3
"""probe_zqcs_rephase.py <repo>/sw/litex <period> <cycles>: DFI commands with the ZQCS period cut to <period>
sys cycles, for LiteDRAM's Refresher, the shipping RegisteredRefresher, the stage without the ZQCS delay, and
the stage with the ZQCS timer's done pulse delayed one cycle instead of its start (the alternative the round-4
ruling names). Prints each variant's ZQCS cycles and whether its commands equal LiteDRAM's one cycle later."""
import math
import sys

sys.path.insert(0, sys.argv[1])
import milan_soc  # noqa: E402
import test_soc_timing_cuts as t  # noqa: E402
import litedram.core.refresher as refresher_module  # noqa: E402
from litedram.core.refresher import Refresher, RefreshTimer  # noqa: E402
from migen import If, Signal  # noqa: E402

PERIOD, CYCLES = int(sys.argv[2]), int(sys.argv[3])
t.ZQCS_PERIOD = PERIOD


class DoneDelayedTimer(RefreshTimer):
    """RefreshTimer whose `done` output is its count-zero compare one cycle late; it reloads on its own compare."""

    def __init__(self, trefi):
        self.wait, self.done, self.count = Signal(), Signal(), Signal(bits_for(trefi))
        done, count = Signal(), Signal(bits_for(trefi), reset=trefi - 1)
        self.sync += [If(self.wait & ~done, count.eq(count - 1)).Else(count.eq(count.reset)), self.done.eq(done)]
        self.comb += [done.eq(count == 0), self.count.eq(count)]


from migen.fhdl.bitcontainer import bits_for  # noqa: E402


class DoneDelayed(t.UndelayedZQCSRefresher):
    """The request registered, and LiteDRAM's ZQCS timer built as DoneDelayedTimer."""

    def __init__(self, settings, clk_freq, zqcs_freq=1e0, postponing=1):
        zqcs_cycles = int(clk_freq / zqcs_freq)
        original = refresher_module.RefreshTimer
        refresher_module.RefreshTimer = lambda n: DoneDelayedTimer(n) if n == zqcs_cycles else original(n)
        try:
            t.UndelayedZQCSRefresher.__init__(self, settings, clk_freq, zqcs_freq, postponing)
        finally:
            refresher_module.RefreshTimer = original


print(f"zqcs period {PERIOD}, gcd with tREFI 782 = {math.gcd(782, PERIOD)}, {CYCLES} cycles")
plain = t.dfi_commands(t.short_zqcs(Refresher), CYCLES)
shifted = [(c + 1, i, n, a) for c, i, n, a in plain if c + 1 < CYCLES]
print(f"plain: ZQCS at {[c for c, _, n, _ in plain if n == 'ZQCS']}, REFRESH {sum(n == 'REFRESH' for _, _, n, _ in plain)}")
for label, cls in (("shipping", milan_soc.RegisteredRefresher), ("undelayed", t.UndelayedZQCSRefresher),
                   ("done-delayed", DoneDelayed)):
    cmds = t.dfi_commands(t.short_zqcs(cls), CYCLES)
    print(f"{label}: ZQCS at {[c for c, _, n, _ in cmds if n == 'ZQCS']}; equals plain + 1: {cmds == shifted}")

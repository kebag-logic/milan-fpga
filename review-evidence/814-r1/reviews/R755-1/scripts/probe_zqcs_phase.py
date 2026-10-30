#!/usr/bin/env python3
"""Reviewer probe: does the registered refresher change when LiteDRAM issues a ZQCS?

Usage: probe_zqcs_phase.py <repo-root>

LiteDRAM's ZQCS timer emits a one-cycle pulse every Z = int(clk_freq/zqcs_freq)
cycles, and the refresh FSM starts a ZQCS only if that pulse falls on the cycle
the refresh sequencer reports done. Both timers run free from reset, so on an
idle controller the sequencer's done falls at a fixed offset k after each tREFI
timer pulse, and a ZQCS can ever occur only if gcd(Z, tREFI) divides the phase
difference. This measures k for LiteDRAM's own refresher and for the shipping
RegisteredRefresher on the gate's own DramSoC (the board's DDR3 part, 100 MHz),
and evaluates that condition for each.
"""
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "litex"))

from migen import run_simulation  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402
import test_soc_timing_cuts as gate  # noqa: E402


def measure(stage):
    soc = gate.build(gate.DramSoC, stage=stage, name="RegisteredRefresher")
    outer = soc.sdram.controller.refresher
    inner = getattr(outer, "refresher", outer)
    seen = {"timer": [], "seq": [], "zq": []}

    def mon():
        for cycle in range(2600):
            if (yield inner.timer.done):
                seen["timer"].append(cycle)
            if (yield inner.sequencer.done):
                seen["seq"].append(cycle)
            if (yield inner.zqcs_timer.done):
                seen["zq"].append(cycle)
            yield
    run_simulation(soc, {"sys": [mon()]}, clocks={"milan": 20, "sys": 10})
    trefi = soc.sdram.controller.settings.timing.tREFI
    z = int(100e6 / soc.sdram.controller.settings.refresh_zqcs_freq)
    zq_first = inner.zqcs_timer.count.reset.value  # first pulse when the count reaches 0
    return seen, trefi, z, zq_first


rows = []
for label, stage in (("LiteDRAM Refresher", Refresher), ("RegisteredRefresher (shipping)", None)):
    seen, trefi, z, zq_first = measure(stage)
    k = [s - t for t, s in zip(seen["timer"], seen["seq"])]
    g = math.gcd(z, trefi)
    # sequencer done at t_m = timer_first + m*trefi + k ; ZQCS pulse at zq_first + n*z
    t0 = seen["timer"][0]
    reachable = ((zq_first - (t0 + k[0])) % g) == 0 if k else None
    rows.append((label, trefi, z, g, t0, k, reachable))
    print(f"{label}: tREFI={trefi} Z={z} gcd={g} first timer pulse={t0} sequencer-done offsets k={k} "
          f"first ZQCS pulse at {zq_first}; idle ZQCS ever coincides: {reachable}")
print("RESULT: measured")

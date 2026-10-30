#!/usr/bin/env python3
"""Probe: does the registered refresher change WHEN LiteDRAM's ZQCS can fire?

LiteDRAM issues ZQCS only when the free-running ZQCS timer's one-cycle pulse
lands on the cycle the refresh sequencer reports done. Both timers run from
reset. This builds the test's DramSoC (shipping add_staged_sdram, 100 MHz,
MT41J256M16 1:4) with the staged and with LiteDRAM's own refresher, records
the sequencer-done cycles over an idle window, and solves the coincidence
condition analytically for the real tREFI and ZQCS period.

Usage: python3 probe_zqcs_phase.py <repo>/sw/litex
"""
import math
import sys

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402
from litedram.core.refresher import Refresher  # noqa: E402
from migen import run_simulation  # noqa: E402


def measure(stage):
    soc = t.build(t.DramSoC, stage=stage, name="RegisteredRefresher")
    outer = soc.sdram.controller.refresher
    inner = getattr(outer, "refresher", outer)
    seq_done, timer_done, zq_done = [], [], []
    trefi = soc.sdram.controller.settings.timing.tREFI
    zq_period = int(soc.sdram.controller.settings.refresh_zqcs_freq and
                    t.SYS_HZ / soc.sdram.controller.settings.refresh_zqcs_freq)

    def mon():
        for cycle in range(2600):
            if (yield inner.sequencer.done):
                seq_done.append(cycle)
            if (yield inner.timer.done):
                timer_done.append(cycle)
            if (yield inner.zqcs_timer.done):
                zq_done.append(cycle)
            yield
    run_simulation(soc, {"sys": [mon()]}, clocks={"milan": 20, "sys": 10})
    return trefi, zq_period, seq_done, timer_done, zq_done


for label, stage in (("staged", None), ("plain", Refresher)):
    trefi, n, seq, tim, zq = measure(stage)
    g = math.gcd(trefi, n)
    # zqcs pulse at n-1 + m*n; sequencer done at seq[0] + k*trefi (idle)
    residue = (seq[0] - (n - 1)) % g
    print(f"{label}: tREFI={trefi} zqcs_period={n} gcd={g} timer_done={tim[:3]} "
          f"sequencer_done={seq[:3]} spacing={[b - a for a, b in zip(seq, seq[1:])]} "
          f"residue={residue} idle_zqcs_possible={residue == 0}")
    if residue == 0:
        # first coincidence: smallest c = seq0 + k*trefi with (c - (n-1)) % n == 0
        k = 0
        # solve k*trefi = (n-1-seq0) mod n
        a, b, m = trefi // g, ((n - 1 - seq[0]) % n) // g, n // g
        k = (b * pow(a, -1, m)) % m
        first = seq[0] + k * trefi
        print(f"{label}: first idle ZQCS at sys cycle {first} = {first / t.SYS_HZ:.3f} s, "
              f"then every {trefi * n // g} cycles = {trefi * n // g / t.SYS_HZ:.3f} s (until the first ZQCS re-phases the timer)")
print("RESULT: DONE")

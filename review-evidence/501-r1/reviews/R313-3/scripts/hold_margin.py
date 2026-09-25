#!/usr/bin/env python3
"""Reviewer probe (R313-1): re-evaluate the capture-hold copy model at 8x8.

Usage: python3 hold_margin.py <figures_base.json> <figures_head.json>

Model and constants are those stated in docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
section 17 ("Timing"): six instructions and two DDR accesses per copied byte,
about 50 instructions per record walked, 10 cycles per instruction and 30 per
DDR access, the shipping 50 MHz CPU clock, and "twice both costs" as the
pessimistic bound, against the 50 ms T_HOLD_MS_P. The copy in
milan_baremetal.c nvm_capture() runs to NVM_AREA_RAW under the hold.
"""
import json
import sys

HOLD_MS, HZ = 50.0, 50e6
for label, path in (("base", sys.argv[1]), ("head", sys.argv[2])):
    for stem in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
        f = json.load(open(path))[stem]
        area = sum(r[4] for r in f["records"])
        nrec = f["nrec"]
        instr = 6 * area + 50 * nrec
        ddr = 2 * area
        cycles = 10 * instr + 30 * ddr
        ms = cycles / HZ * 1000
        print(f"{label} {stem}: area {area} B, {nrec} records -> {instr} instr, "
              f"{ddr} DDR, {cycles} cycles, {ms:.1f} ms nominal, {2 * ms:.1f} ms at 2x; "
              f"hold margin {HOLD_MS / ms:.2f}x nominal, {HOLD_MS / (2 * ms):.2f}x at 2x"
              f"{'  <-- 2x EXCEEDS the 50 ms hold' if 2 * ms > HOLD_MS else ''}")

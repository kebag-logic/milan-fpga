#!/usr/bin/env python3
"""[R312] probe: re-evaluate docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
section 18's capture-copy cost model (6 instructions/byte, 50/record,
2 DDR accesses/byte, 10 cycles/instruction, 30 cycles/DDR access, 50 MHz
CPU, and the page's 'twice both costs' bound) at the base and head 8x8
record areas, against the shipping T_HOLD_MS_P = 50 ms."""
def model(area, nrec, k=1):
    ins = 6 * area + 50 * nrec; ddr = 2 * area
    cyc = k * (10 * ins + 30 * ddr)
    return ins, ddr, cyc, cyc / 50e6 * 1e3
for label, area in (("base 8x8 (page's figure)", 8604), ("head 8x8 (this PR)", 12634)):
    for k in (1, 2):
        ins, ddr, cyc, ms = model(area, 156, k)
        print(f"{label}: area={area} x{k}: instr={ins} ddr={ddr} cycles={cyc} copy={ms:.1f} ms margin_to_50ms={50/ms:.2f}x")

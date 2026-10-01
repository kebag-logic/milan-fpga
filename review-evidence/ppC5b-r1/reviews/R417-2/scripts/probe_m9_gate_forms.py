#!/usr/bin/env python3
"""R417-2 probe: feed check_m9_opcodes.py's parser forms its selftest does not
cover and report whether the gate passes (silent) or fails (loud).
Usage: probe_m9_gate_forms.py <path-to-clone>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import check_m9_opcodes as g

BASE = ("localparam logic [15:0] OP_READ_DESCRIPTOR_C = 16'h0004;\n"
        "localparam logic [15:0] OP_SET_NAME_C = 16'h0010;\n")
GOOD = "static const uint16_t kOpcodes[] = { 0x0004, 0x0010, };"
CASES = [
    ("control: equal sets", BASE, GOOD, "pass"),
    ("comma list hides a second OP_*_C", BASE +
     "localparam logic [15:0] OP_GET_NAME_C = 16'h0011, OP_X_C = 16'h0012;\n", GOOD, "fail"),
    ("lower-case 16'h with spaces", BASE +
     "localparam logic [15:0] OP_GET_NAME_C = 16'h 0011;\n", GOOD, "fail"),
    ("11-bit width", BASE + "localparam logic [10:0] OP_GET_NAME_C = 11'h011;\n", GOOD, "fail"),
    ("decimal radix", BASE + "localparam logic [15:0] OP_GET_NAME_C = 16'd17;\n", GOOD, "fail"),
    ("parameter instead of localparam", BASE +
     "parameter logic [15:0] OP_GET_NAME_C = 16'h0011;\n", GOOD, "fail"),
    ("multi-line declaration", BASE +
     "localparam logic [15:0]\n    OP_GET_NAME_C = 16'h0011;\n", GOOD, "fail"),
    ("block-commented OP_*_C", BASE +
     "/* localparam logic [15:0] OP_GET_NAME_C = 16'h0011; */\n", GOOD, "fail"),
    ("line-commented OP_*_C", BASE +
     "// localparam logic [15:0] OP_GET_NAME_C = 16'h0011;\n", GOOD, "pass"),
]
bad = 0
for what, eng, bench, want in CASES:
    found, refused = g.engine_opcodes(eng)
    problems = g.compare(found, g.bench_opcodes(bench), refused)
    got = "fail" if problems else "pass"
    note = "as expected" if got == want else "UNEXPECTED"
    if got != want:
        bad += 1
    print(f"{what}: gate {got} ({note})")
    for p in problems[:3]:
        print("   ", p.strip())
print(f"probe: {len(CASES)} forms, {bad} unexpected")

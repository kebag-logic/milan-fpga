#!/usr/bin/env python3
"""Probe scripts/check_m9_opcodes.py of a processor checkout (argv[1]) with
declaration forms inserted into a copy of the real engine text, against the
real tb/pp_top kOpcodes. Read-only: nothing in the checkout is written.
Each form states whether the gate must fail (an arm that M9 does not sweep, or
a form the gate cannot read) or must pass. Exit 0 when every form behaves."""
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('g', root / 'scripts' / 'check_m9_opcodes.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
eng = (root / 'hdl/aecp/KL_aecp_engine.sv').read_text()
bench = g.bench_opcodes((root / 'tb/pp_top/sim_main.cpp').read_text())
anchor = 'localparam logic [15:0] OP_'
i = eng.index(anchor)
FORMS = [
    ('head as is', '', True),
    ('localparam canonical new opcode 0x0077', "localparam logic [15:0] OP_PROBE_NEW_C = 16'h0077;\n", False),
    ('parameter keyword (R417-2 S1)', "parameter logic [15:0] OP_PROBE_NEW_C = 16'h0077;\n", False),
    ('parameter, no type', "parameter OP_PROBE_NEW_C = 16'h0077;\n", False),
    ('localparam without logic', "localparam [15:0] OP_PROBE_NEW_C = 16'h0077;\n", False),
    ('localparam int decimal', "localparam int OP_PROBE_NEW_C = 119;\n", False),
    ('localparam 16-bit decimal', "localparam logic [15:0] OP_PROBE_NEW_C = 16'd119;\n", False),
    ('two names in one declaration', "localparam logic [15:0] OP_PROBE_A_C = 16'h0077, OP_PROBE_B_C = 16'h0078;\n", False),
    ('parameter in a #( ) port list', "module m #(parameter logic [15:0] OP_PROBE_NEW_C = 16'h0077) ();\n", False),
    ('a duplicate name for 0x0004', "localparam logic [15:0] OP_PROBE_DUP_C = 16'h0004;\n", False),
    ('line comment only (not a declaration)', "// localparam logic [15:0] OP_PROBE_NEW_C = 16'h0077;\n", True),
    ('non-opcode GDI localparam', "localparam logic [15:0] GDI_PROBE_C = 16'h0077;\n", True),
    ('a reference to an OP_*_C on a right-hand side', "localparam logic [15:0] GDI_PROBE_C = OP_READ_DESCRIPTOR_C;\n", True),
    ('canonical, upper-case hex and spaces before ;', "localparam logic [15:0] OP_PROBE_NEW_C = 16'H0077 ;\n", False),
]
bad = 0
for what, ins, want_pass in FORMS:
    found, refused = g.engine_opcodes(eng[:i] + ins + eng[i:])
    probs = g.compare(found, bench, refused)
    passed = not probs
    ok = passed == want_pass
    bad += not ok
    print(f"{'OK ' if ok else 'UNEXPECTED'} {what}: gate {'PASS' if passed else 'FAIL'} (want {'PASS' if want_pass else 'FAIL'})"
          + ('' if passed else f" - {probs[0].strip()[:90]}"))
print(f'{len(FORMS)} forms, {bad} unexpected; engine opcodes at head {len(g.engine_opcodes(eng)[0])}, kOpcodes {len(bench)}')
sys.exit(1 if bad else 0)

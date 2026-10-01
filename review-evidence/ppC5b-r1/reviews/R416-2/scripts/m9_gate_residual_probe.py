#!/usr/bin/env python3
"""Reviewer probe: feed check_m9_opcodes.py's own parse two engine texts and
show which OP_*_C names each sees. Run from the root of an exported tree."""
import importlib.util
spec = importlib.util.spec_from_file_location("g", "scripts/check_m9_opcodes.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
bench = "static const uint16_t kOpcodes[] = { 0x0004, };"
cases = {
    "one declarator per statement (the engine's form)":
        "localparam logic [15:0] OP_READ_DESCRIPTOR_C = 16'h0004;\n"
        "localparam logic [15:0] OP_SET_NAME_C = 16'h0010;\n",
    "a well-formed opcode plus two declarators in one statement":
        "localparam logic [15:0] OP_READ_DESCRIPTOR_C = 16'h0004;\n"
        "localparam logic [15:0] OP_GET_NAME_C = 16'h0011, OP_SET_NAME_C = 16'h0010;\n",
}
for what, eng in cases.items():
    found, refused = g.engine_opcodes(eng)
    problems = g.compare(found, g.bench_opcodes(bench), refused)
    print(f"{what}: parsed {sorted(hex(k) for k in found)}, gate "
          f"{'FAIL' if problems else 'PASS'}")
    for p in problems:
        print("   " + p.strip())

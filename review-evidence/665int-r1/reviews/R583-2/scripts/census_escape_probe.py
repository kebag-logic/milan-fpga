#!/usr/bin/env python3
"""Reviewer probe: plant reads of a class-D wire, in SystemVerilog forms the
census's docstring says it covers (a condition, a port connection) or that a
datapath edit could use, into copies of milan_datapath.sv, route each to the
CRF talker's C-TAG enable (the wire), and record whether
publication_census.py --check refuses the copy. Usage:
  python3 -I census_escape_probe.py <repo> <scratch-dir>
Exit 0 always; the table is the result."""
import subprocess, sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
src = (repo / "hdl/milan/milan_datapath.sv").read_text(encoding="utf-8")
ANCHOR = "    .vlan_en_i  (crft_class_a_w),"
assert src.count(ANCHOR) == 1
DECL_ANCHOR = "  wire crft_class_a_w = (ACMP_SRC_C > N_STREAMS) &"
assert src.count(DECL_ANCHOR) == 1
W = "pp_cd_srp_over_limit_w"
PLANTS = {
    "control: named port, rhs (expected caught)": (
        f"  wire probe_w;\n  assign probe_w = {W};\n", "probe_w"),
    "case-item label in an always_comb": (
        "  logic probe_w;\n  always_comb begin\n    probe_w = 1'b0;\n    unique case (1'b1)\n"
        f"      {W}: probe_w = 1'b1;\n      default: probe_w = 1'b0;\n    endcase\n  end\n", "probe_w"),
    "positional port connection": (
        f"  wire probe_w;\n  KL_probe_buf u_probe_pos ({W}, probe_w);\n", "probe_w"),
    "implicit .name port connection": (
        f"  wire probe_w;\n  KL_probe_buf u_probe_dot (.{W}, .y_o(probe_w));\n", "probe_w"),
    "function body return": (
        f"  function automatic logic probe_f();\n    return {W};\n  endfunction\n"
        "  wire probe_w;\n  assign probe_w = probe_f();\n", "probe_w"),
}
rows = []
for name, (decl, sig) in PLANTS.items():
    text = src.replace(DECL_ANCHOR, decl + DECL_ANCHOR, 1).replace(
        ANCHOR, f"    .vlan_en_i  (crft_class_a_w & ~{sig}),", 1)
    path = scratch / (name.split(":")[0].replace(" ", "_").replace(".", "") + ".sv")
    path.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-B", str(repo / "sw/mailbox/publication_census.py"),
                        "--check", "--datapath", str(path)], capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith("[FAIL]")]
    verdict = "REFUSED" if r.returncode else "ACCEPTED (escape)"
    rows.append((name, r.returncode, verdict, fails[0][:160] if fails else ""))
for name, rc, verdict, f in rows:
    print(f"{name:45} rc={rc} {verdict:18} {f}")

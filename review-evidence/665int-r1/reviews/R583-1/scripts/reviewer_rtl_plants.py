#!/usr/bin/env python3
"""Reviewer RTL plants for the publication block (R583-1), run through the
suite's own mutants.py machinery (planted copy, Makefile recipe, named check).

Usage: python3 reviewer_rtl_plants.py <repo-root> <keep-dir> [jobs]
Each arm must be caught: the harness exits 1 with a [FAIL] line naming the
needle. Exit 0 when every arm is caught, 1 otherwise.
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
keep = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(root / "tb" / "verilator" / "mbx"))
import mutants  # noqa: E402  (the suite's own driver, read from the tree under review)

A = mutants.Arm
ARMS = (
    A("rv-pub-sid-hi-not-reset", "KL_mbx.sv", "          pub_sid_hi_r[i][k] <= '0;\n", "", 0,
      "P5 a reset clears every publication register"),
    A("rv-pub-binding-sid-valid-unmasked-away", "KL_mbx.sv",
      "pub_binding_r[pub_if_w][pub_k_w] <= 2'(host_wdata_i & (mbx_place_f(32'hFFFF_FFFF, MBX_BINDING_BOUND_LSB_C, "
      "MBX_BINDING_BOUND_WIDTH_C) | mbx_place_f(32'hFFFF_FFFF, MBX_BINDING_SID_VALID_LSB_C, "
      "MBX_BINDING_SID_VALID_WIDTH_C)));",
      "pub_binding_r[pub_if_w][pub_k_w] <= 2'(host_wdata_i & (mbx_place_f(32'hFFFF_FFFF, MBX_BINDING_BOUND_LSB_C, "
      "MBX_BINDING_BOUND_WIDTH_C)));", 0, "P1 DA_GATE keeps OPEN"),
    A("rv-pub-licence-out-from-da-gate", "KL_mbx.sv",
      "MBX_N_PUB_SOURCES_C'(mbx_field_f(32'(pub_licence_r[i]),",
      "MBX_N_PUB_SOURCES_C'(mbx_field_f(32'(pub_da_gate_r[i]),", 1, "P2 every field reaches the datapath"),
    A("rv-pub-read-ignores-decode", "KL_mbx.sv",
      "if (pub_at_w && !pub_sink_w && pub_reg_w == AW2_C'(MBX_PUB_REG_DA_GATE_C)) reg_rdata_w",
      "if (!pub_sink_w && pub_reg_w == AW2_C'(MBX_PUB_REG_DA_GATE_C) && off_w >= AW2_C'(MBX_PUB_BASE_C)) "
      "reg_rdata_w", 0, "P4 every hole of every interface block"),
    A("rv-pub-slope-readback-of-if0", "KL_mbx.sv",
      "reg_rdata_w = 32'(pub_idle_slope_r[pub_if_w]);", "reg_rdata_w = 32'(pub_idle_slope_r[0]);", 0,
      "P1 each interface's registers", 2),
    A("rv-pub-da-gate-write-to-if0", "KL_mbx.sv",
      "pub_da_gate_r[pub_if_w] <= 16'(", "pub_da_gate_r[0] <= 16'(", 1, "P1 each interface's registers", 2),
    A("rv-pub-reset-interface-0-only", "KL_mbx.sv",
      "    if (!rst_n) begin\n      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin\n        pub_da_gate_r[i] <= '0;",
      "    if (!rst_n) begin\n      for (int i = 0; i < 1; i++) begin\n        pub_da_gate_r[i] <= '0;", 0,
      "P5 a reset clears every publication register", 2),
    A("rv-pub-sink-k-from-entry-low-bit", "KL_mbx.sv",
      "pub_k_w    = PUB_KW_C'(entry);", "pub_k_w    = PUB_KW_C'(entry & 'h7);", 0,
      "P1 each interface's registers and each sink's entry"),
)

with ThreadPoolExecutor(max_workers=jobs) as pool:
    results = list(pool.map(lambda a: mutants.run_arm(a, keep), ARMS))
bad = 0
for arm, caught, detail in results:
    print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name} (host {arm.host}, {arm.ifs} if): {detail}")
    bad += not caught
print(f"reviewer RTL plants: {len(ARMS) - bad} of {len(ARMS)} caught")
sys.exit(1 if bad else 0)

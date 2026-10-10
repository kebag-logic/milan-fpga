#!/usr/bin/env python3
"""reviewer_rtl_plants.py - the reviewer's own planted KL_mbx defects on the
round-3 values (STARTED, TALKER_DECL), beyond tb/verilator/mbx/mutants.py,
built and graded by the head's own mutants.plant/run_arm (a plant is caught
only when the suite exits 1 with a [FAIL] line holding the expected words).
Usage: VERILATOR=<verilator> python3 -B reviewer_rtl_plants.py <tree> <scratch>"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "tb/verilator/mbx"))
import mutants as mu  # noqa: E402
OUT = ("        pub_started_o[MBX_N_PUB_SINKS_C*i + k] = mbx_field_f(32'(pub_binding_r[i][k]), "
       "MBX_BINDING_STARTED_LSB_C, MBX_BINDING_STARTED_WIDTH_C) != 0;")
ARMS = (
    # STARTED forced low while SID_VALID is set: a started move that keeps the stream is lost
    mu.Arm("rv-started-masked-by-sid-valid", "KL_mbx.sv", OUT,
           OUT.replace("!= 0;", "!= 0 && !pub_sid_valid_o[MBX_N_PUB_SINKS_C*i + k];"), 0, "P3 STARTED moves"),
    # TALKER_DECL's read-back dropped from the register mux (the output still driven)
    mu.Arm("rv-talker-decl-not-read-back", "KL_mbx.sv",
           "    if (pub_at_w && !pub_sink_w && pub_reg_w == AW2_C'(MBX_PUB_REG_TALKER_DECL_C)) "
           "reg_rdata_w = 32'(pub_talker_decl_r[pub_if_w]);\n", "", 0, "P1"),
    # TALKER_DECL written to interface 0 whichever interface is addressed (two interfaces)
    mu.Arm("rv-talker-decl-on-interface-0", "KL_mbx.sv",
           "        pub_talker_decl_r[pub_if_w] <= 16'(", "        pub_talker_decl_r[0] <= 16'(", 1, "P", 2),
)
scratch.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    res = list(pool.map(lambda a: mu.run_arm(a, scratch), ARMS))
for arm, caught, detail in res:
    print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name} (ifs {arm.ifs}, host {arm.host}): {detail}")
print(f"reviewer RTL plants: {sum(c for _, c, _ in res)} of {len(res)} caught")

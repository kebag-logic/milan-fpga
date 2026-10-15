#!/usr/bin/env python3
"""Scratch: run settle_control.py's own harness on planted copies of the bind arm.

usage: plant_sc.py <repo> <simulator> <out>
Each plant edits one line of the extracted block; each must end in its named $fatal.
"""
import importlib.util
import sys
from pathlib import Path

repo, sim, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("settle_control", repo / "tb/verilator/follow_ring/settle_control.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)
text = (repo / "hdl/milan/milan_datapath.sv").read_text()
begin = text.index("  localparam int unsigned SRC_SETTLE_ERR_C")
end = text.index("  end : g_settle_recentre", begin) + len("  end : g_settle_recentre")
block = text[begin:end]
PDU = "      settle_bind_pdu_w[s] = settle_bind_wait_r[s] && lb_tap_tvalid_w &&\n"
TAIL = "                             lb_tap_tlast_w && (32'(lb_tap_tuser_w) == s);\n"
ARM = "  wire settle_bind_arm_w = !follow_sel_r && (|settle_bind_pdu_w);\n"
WAIT = ("    else settle_bind_wait_r <= (settle_bind_wait_r | strtbl_bind_rise_w[LB_STREAMS_C-1:0]) &\n"
        "                               ~settle_bind_pdu_w & ~strtbl_bind_fall_w[LB_STREAMS_C-1:0];\n")
PLANTS = (
    ("no-wait", PDU, "      settle_bind_pdu_w[s] = lb_tap_tvalid_w &&\n", "a PDU without a bind armed"),
    ("any-stream", TAIL, "                             lb_tap_tlast_w;\n", "another stream's PDU armed"),
    ("any-beat", TAIL, "                             (32'(lb_tap_tuser_w) == s);\n", "a beat before the PDU's end armed"),
    ("keep-wait", WAIT, "    else settle_bind_wait_r <= (settle_bind_wait_r | strtbl_bind_rise_w[LB_STREAMS_C-1:0]) &\n"
                        "                               ~strtbl_bind_fall_w[LB_STREAMS_C-1:0];\n", "a later PDU armed again"),
    ("fall-ignored", WAIT, "    else settle_bind_wait_r <= (settle_bind_wait_r | strtbl_bind_rise_w[LB_STREAMS_C-1:0]) &\n"
                           "                               ~settle_bind_pdu_w;\n", "an unbound stream's PDU armed"),
    ("ungated", ARM, "  wire settle_bind_arm_w = (|settle_bind_pdu_w);\n", "a bind under following armed"),
    ("at-rise", ARM, "  wire settle_bind_arm_w = !follow_sel_r && (|strtbl_bind_rise_w[LB_STREAMS_C-1:0]);\n",
     "the bind armed before its first PDU"),
    ("no-arm", ARM, "  wire settle_bind_arm_w = 1'b0;\n", "the bind's first PDU did not arm"),
)
fails = 0
for name, old, new, expect in PLANTS:
    assert block.count(old) == 1, name
    work = out / name
    work.mkdir(parents=True, exist_ok=True)
    rc = sc.run(6250000, block.replace(old, new), work, sim)
    log = (work / "6250000" / "run.log").read_text() if (work / "6250000" / "run.log").exists() else ""
    caught = rc != 0 and expect in log
    fails += not caught
    print(f"[PLANT] {name}: {'caught' if caught else 'SURVIVED'} by \"{expect}\" (rc {rc})", flush=True)
print(f"settle_control bind plants: {len(PLANTS) - fails}/{len(PLANTS)} caught")
sys.exit(1 if fails else 0)

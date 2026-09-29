#!/usr/bin/env python3
"""Scratch: the issue #65 arms as srp_top patches (one file each)."""
import subprocess, sys, tempfile
from pathlib import Path
REPO = Path(sys.argv[1])
SPECS = {
    "licence-ignores-join": ("hdl/srp/KL_srp_talker_fsm.sv", [(
        "                 && sr_admitted_i[s] && vid_ok_w[s];\n",
        "                 && sr_admitted_i[s];\n")]),
    "join-sent-at-handover": ("hdl/srp/KL_srp_vlan.sv", [(
        "            if (ev_code_r == EV_NEW_C) queued_r[free_ix_r] <= 1'b1;\n",
        "            if (ev_code_r == EV_NEW_C) sent_r[free_ix_r] <= 1'b1;\n")]),
    "count-up-unsends": ("hdl/srp/KL_srp_vlan.sv", [(
        "              st_r <= V_IDLE;                      // count up, silent\n",
        "              sent_r[found_ix_r] <= 1'b0;\n"
        "              st_r <= V_IDLE;                      // count up, silent\n")]),
    "tx-strobe-any-app": ("hdl/srp/KL_srp_encoder.sv", [(
        "  assign tx_mvrp_o     = (st_r == E_TXREQ) && txreq_ready_i && (cur_app_r == APP_MVRP_C);\n",
        "  assign tx_mvrp_o     = (st_r == E_TXREQ) && txreq_ready_i;\n")]),
    "listener-lane-cut": ("hdl/srp/KL_srp_top.sv", [(
        "  assign vu_sel_ls_w       = ls_user_valid_w && (!tk_user_valid_w || vrr_r);\n",
        "  assign vu_sel_ls_w       = 1'b0;\n")]),
}
for label, (rel, reps) in SPECS.items():
    text = (REPO / rel).read_text(); new = text
    for old, rep in reps:
        assert new.count(old) == 1, (label, old)
        new = new.replace(old, rep)
    with tempfile.TemporaryDirectory() as tmp:
        a, b = Path(tmp) / "a", Path(tmp) / "b"; a.write_text(text); b.write_text(new)
        res = subprocess.run(["diff", "-u", "--label", f"a/{rel}", "--label", f"b/{rel}", str(a), str(b)],
                             capture_output=True, text=True)
    assert res.returncode == 1
    (REPO / "tb/srp_top/mutations" / f"{label}.patch").write_text(res.stdout)
    print("wrote", label)

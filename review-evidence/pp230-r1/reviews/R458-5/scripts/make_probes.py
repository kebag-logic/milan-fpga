#!/usr/bin/env python3
"""Generate the R458-5 reviewer probes as git-apply patches against a tree.

usage: make_probes.py <tree> <out-dir>
Each probe is one exact string replacement in one HDL file; a probe whose
anchor is not found exactly once is refused.
"""
import difflib
import sys
from pathlib import Path

PROBES = [
    # name, file, old, new
    ("r5-wid-write-ignores-ready", "hdl/srp/KL_srp_talker_fsm.sv",
     "      if (gate_open_acc_w) begin\n        wid_r[gate_src_i]",
     "      if (rst_n && gate_valid_i && gate_open_i) begin\n        wid_r[gate_src_i]"),
    ("r5-wtsp-mfs-mif-swapped", "hdl/srp/KL_srp_talker_fsm.sv",
     "{gate_max_frame_i, gate_max_interval_i,",
     "{gate_max_interval_i, gate_max_frame_i,"),
    ("r5-tf-tk-written-at-ls-pointer", "hdl/srp/KL_srp_top.sv",
     "      tf_tk_ram_r[tf_wptr_r[0]]",
     "      tf_tk_ram_r[tf_wptr_r[1]]"),
    ("r5-tf-ls-read-at-tk-rptr", "hdl/srp/KL_srp_top.sv",
     "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];",
     "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[0]];"),
    ("r5-wsid-read-xor-1", "hdl/srp/KL_srp_listener_fsm.sv",
     "assign wsid_w = wsid_r[wsrc_r];",
     "assign wsid_w = wsid_r[wsrc_r ^ SNK_W_C'(1)];"),
    ("r5-wsid-written-at-walk-index", "hdl/srp/KL_srp_listener_fsm.sv",
     "        wsid_r[ctl_sink_i] <= ctl_stream_id_i;",
     "        wsid_r[wsrc_r] <= ctl_stream_id_i;"),
    ("r5-granted-slope-at-stage-index", "hdl/srp/KL_srp_admission.sv",
     "wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[aidx_r] : 32'd0;",
     "wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[cidx_q2_r] : 32'd0;"),
    ("r5-wid-ram-vid-from-da", "hdl/srp/KL_srp_talker_fsm.sv",
     "wid_r[gate_src_i] <= {gate_stream_id_i, gate_da_i, gate_vid_i};",
     "wid_r[gate_src_i] <= {gate_stream_id_i, gate_da_i, gate_da_i[11:0]};"),
    # expected-equivalent probes: no committed test should be able to see them
    ("r5-eq-slope-write-only-when-valid", "hdl/srp/KL_srp_admission.sv",
     "    if (rst_n) begin\n      slope_q_r[cidx_q2_r]",
     "    if (rst_n && valid_q2_r) begin\n      slope_q_r[cidx_q2_r]"),
    ("r5-eq-wtsp-write-in-reset", "hdl/srp/KL_srp_talker_fsm.sv",
     "assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
     "assign gate_open_acc_w = gate_acc_w && gate_open_i;"),
]


def main() -> int:
    tree, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, rel, old, new in PROBES:
        text = (tree / rel).read_text()
        if text.count(old) != 1:
            print(f"REFUSED {name}: anchor found {text.count(old)} times", file=sys.stderr)
            return 1
        after = text.replace(old, new)
        diff = difflib.unified_diff(text.splitlines(keepends=True), after.splitlines(keepends=True),
                                    fromfile="a/" + rel, tofile="b/" + rel, n=3)
        (out / (name + ".patch")).write_text("".join(diff))
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

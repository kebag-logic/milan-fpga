#!/usr/bin/env python3
"""Reviewer mutants against the milan_dp split leg: the paths its 48 checks do not name.

Usage: VERILATOR=<verilator> python3 split_reviewer_mutants.py <repo-root> <work-dir> [--jobs N]
Each arm edits a COPY of one split source (never the tracked file), builds the
split leg through its own recipe (make build-split with DP_SRC / CDC_SRC /
CTLS_SRC pointing at the copy, SPLIT_MDIR under <work-dir>), runs it and
records whether the leg fails. "SURVIVED" means the leg passes with the
defect in place: no check detects it. Arms run in parallel (--jobs).
"""
import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("work", type=Path)
ap.add_argument("--jobs", type=int, default=4)
args = ap.parse_args()
TB = args.root / "tb/verilator/milan_dp"
DP = args.root / "hdl/milan/milan_datapath.sv"
CDC = args.root / "hdl/milan/mailbox/KL_mbx_cdc.sv"
CTLS = args.root / "hdl/milan/KL_ctrl_split.sv"
VAR = {DP: "DP_SRC", CDC: "CDC_SRC", CTLS: "CTLS_SRC"}

ARMS = (
    ("E1 the AVB_INFO change event never leaves the datapath", DP,
     "    assign o_ctl_avb_chg_p     = gsi_avb_chg_w;", "    assign o_ctl_avb_chg_p     = 1'b0;"),
    ("E2 the counter-change descriptor never leaves the datapath", DP,
     "    assign o_ctl_ctr_chg_valid = pp_ctr_evt_valid_w;", "    assign o_ctl_ctr_chg_valid = 1'b0;"),
    ("E3 the live map-write event never leaves the datapath", DP,
     "    assign o_ctl_amap_wr_p     = amap_edit_live_wr_p;", "    assign o_ctl_amap_wr_p     = 1'b0;"),
    ("G1 the grandmaster identity crosses as zero", CDC,
     "      ev_gm_r   <= d_gm_id_i;", "      ev_gm_r   <= 64'd0;"),
    ("G2 the grandmaster change never leaves the datapath", DP,
     "    assign o_ctl_gm_change_p = pp_gm_change_p_w;", "    assign o_ctl_gm_change_p = 1'b0;"),
    ("C1 every counter change posted under descriptor index 0", CDC,
     "            mc_index_w = 16'(b - MBX_CTRCHG_FIRST_TBL_C[f]);", "            mc_index_w = 16'd0;"),
    ("W1 the EDIT window's request never reaches the datapath", DP,
     "    assign ppo_amap_edit_req_w        = i_ctl_edit_req;", "    assign ppo_amap_edit_req_w        = 1'b0;"),
    ("T1 the tap refuses MSRP at its group address", CTLS,
     "                 || ((da_r == DA_MSRP_C) && (etype_w == ET_MSRP_C))",
     "                 || 1'b0"),
    ("T2 the tap refuses MAAP", CTLS,
     "                         || (subtype_w == ST_ACMP_C) || (subtype_w == ST_MAAP_C)))",
     "                         || (subtype_w == ST_ACMP_C)))"),
    ("D1 the talker declaration published as FAILED, not ADVERTISE", DP,
     "      assign pp_cd_srp_tk_decl_state_w[2*s +: 2] = {1'b0, i_ctl_pub_talker_decl[s]};",
     "      assign pp_cd_srp_tk_decl_state_w[2*s +: 2] = {i_ctl_pub_talker_decl[s], 1'b0};"),
)


def run(arm):
    name, src, old, new = arm
    text = src.read_text()
    if text.count(old) != 1:
        return name, "ANCHOR", "anchor not found once"
    d = args.work / name.split()[0]
    d.mkdir(parents=True, exist_ok=True)
    copy = d / src.name
    copy.write_text(text.replace(old, new))
    mk = ["make", "-s", "--no-print-directory", "-C", str(TB), "build-split", f"SPLIT_MDIR={d / 'obj'}",
          f"{VAR[src]}={copy}", "VERILATOR_JOBS=2"]
    b = subprocess.run(mk, capture_output=True, text=True, env=dict(os.environ))
    if b.returncode:
        return name, "BUILD-FAIL", (b.stdout + b.stderr)[-800:]
    r = subprocess.run([str(d / "obj" / "Vmilan_dp_split")], capture_output=True, text=True, cwd=TB, timeout=1200)
    tally = [ln for ln in r.stdout.splitlines() if ln.startswith("checks:")]
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    return name, ("CAUGHT" if r.returncode else "SURVIVED"), "; ".join(tally + fails[:3])


with ThreadPoolExecutor(args.jobs) as ex:
    results = list(ex.map(run, ARMS))
for name, verdict, detail in results:
    print(f"{verdict:9s} {name}: {detail}")
print(f"survived: {sum(v == 'SURVIVED' for _, v, _ in results)} of {len(results)}")

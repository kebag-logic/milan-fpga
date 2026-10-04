#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer fault probes of the #230 storage paths against the committed suites.

Each probe is one exact text edit of one RTL file (refused unless the old text
occurs exactly once). The probe runs in a disposable copy of hdl/ and the SRP
benches, builds and runs the named suite target, and records its exit status,
its tallies per shape and its FAIL lines. A probe is CAUGHT when the target
exits non-zero with at least one FAIL line, and SURVIVED when it exits 0.

usage: probes.py <tree> <work> <receipts> [--jobs N]
VERILATOR names the simulator.
"""
import argparse
import concurrent.futures
import shutil
import subprocess
from pathlib import Path

T = "hdl/srp/KL_srp_talker_fsm.sv"
L = "hdl/srp/KL_srp_listener_fsm.sv"
A = "hdl/srp/KL_srp_admission.sv"
TOP = "hdl/srp/KL_srp_top.sv"

# label, file, old, new, suite, RUN_ARGS
PROBES = [
    ("p01-wid-ram-write-ignores-ready", T,
     "      if (gate_open_acc_w) begin\n        wid_r[gate_src_i]",
     "      if (rst_n && gate_valid_i && gate_open_i) begin\n        wid_r[gate_src_i]",
     "srp_stream_fsms", "walk"),
    ("p02-wtsp-mfs-mif-swapped", T,
     "    wval_w[143:128] = wtsp_w[67:52];             // MaxFrameSize\n"
     "    wval_w[127:112] = wtsp_w[51:36];",
     "    wval_w[143:128] = wtsp_w[51:36];             // MaxFrameSize\n"
     "    wval_w[127:112] = wtsp_w[67:52];",
     "srp_stream_fsms", "walk"),
    ("p03-wid-vlan-slice-off", T,
     "{4'd0, wid_w[11:0]};", "{4'd0, wid_w[12:1]};", "srp_stream_fsms", "walk"),
    ("p04-wid-da-slice-off", T,
     "wval_w[207:160] = wid_w[59:12];", "wval_w[207:160] = wid_w[60:13];",
     "srp_stream_fsms", "walk"),
    ("p05-wsid-ram-read-at-ctl-sink", L,
     "    assign wsid_w = wsid_r[wsrc_r];", "    assign wsid_w = wsid_r[ctl_sink_i];",
     "srp_stream_fsms", "walk"),
    ("p06-wsid-ram-read-neighbour", L,
     "    assign wsid_w = wsid_r[wsrc_r];", "    assign wsid_w = wsid_r[wsrc_r - 1'b1];",
     "srp_stream_fsms", "walk"),
    ("p07-tf-ls-head-read-ahead", TOP,
     "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];", "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1] + 5'd1];",
     "srp_top", "storage"),
    ("p08-tf-ls-write-at-rptr", TOP,
     "      tf_ls_ram_r[tf_wptr_r[1]]", "      tf_ls_ram_r[tf_rptr_r[1]]",
     "srp_top", "storage"),
    ("p09-tf-tk-written-with-ls-word", TOP,
     "        <= {tk_arm_cancel_w, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w};",
     "        <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};",
     "srp_top", "storage"),
    ("p10-slope-read-at-store-index", A,
     "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r]};",
     "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[cidx_q2_r]};",
     "srp_admission", ""),
    ("p11-granted-slope-of-source-0", A,
     "wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[aidx_r] : 32'd0;",
     "wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[0] : 32'd0;",
     "srp_admission", ""),
    ("p12-wtsp-written-at-walk-source", T,
     "      wtsp_r[gate_src_i] <= {gate_max_frame_i,",
     "      wtsp_r[wsrc_r] <= {gate_max_frame_i,",
     "srp_stream_fsms", "walk"),
]


def trial(tree: Path, work: Path, probe: tuple) -> tuple[str, int, str]:
    label, rel, old, new, suite, args = probe
    copy = work / label
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree / "hdl", copy / "hdl")
    for name in ("common", "srp_top", "srp_stream_fsms", "srp_admission"):
        shutil.copytree(tree / "tb" / name, copy / "tb" / name,
                        ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
    target = copy / rel
    text = target.read_text()
    if text.count(old) != 1:
        return label, -1, f"EDIT NOT UNIQUE ({text.count(old)} matches)"
    target.write_text(text.replace(old, new))
    cmd = ["make", "-C", str(copy / "tb" / suite)] + ([f"RUN_ARGS={args}"] if args else [])
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    return label, res.returncode, res.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("tree", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("receipts", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    a.receipts.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(lambda p: trial(a.tree, a.work, p), PROBES))
    for (label, rc, out), probe in zip(results, PROBES):
        (a.receipts / f"{label}.log").write_text(out)
        tallies = [ln for ln in out.splitlines() if " checks: " in ln or "sources" in ln]
        fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
        verdict = "CAUGHT" if rc not in (0, -1) and fails else ("SURVIVED" if rc == 0 else "INVALID")
        tags = sorted({ln.split(":")[1].strip().split()[0] for ln in fails if ":" in ln})
        print(f"{label} [{probe[4]} {probe[5] or 'default'}]: rc={rc} {verdict} fails={len(fails)} "
              f"tags={','.join(tags)}")
        for t in tallies:
            print(f"    {t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

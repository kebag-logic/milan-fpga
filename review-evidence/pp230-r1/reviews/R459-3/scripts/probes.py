#!/usr/bin/env python3
"""Reviewer probes for the #230 storage paths at exact head b59e99cb.

Each probe is one exact text edit to a copy of the head tree (the edit must
match exactly once), then the named committed suite target is run in that
copy with the pinned simulator. A probe is CAUGHT when the target exits
non-zero with at least one FAIL line and a tally; SURVIVED when it exits 0.
usage: probes.py <head tree> <scratch dir> <receipt dir> [--jobs N]
"""
import concurrent.futures as cf, os, shutil, subprocess, sys
from pathlib import Path

TK = "hdl/srp/KL_srp_talker_fsm.sv"; LS = "hdl/srp/KL_srp_listener_fsm.sv"
AD = "hdl/srp/KL_srp_admission.sv"; TOP = "hdl/srp/KL_srp_top.sv"
# label, file, old, new, suite, make args
PROBES = [
 ("tf-ls-head-read-ahead", TOP, "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];",
  "tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1] + 5'd1];", "srp_top", "RUN_ARGS=storage"),
 ("tf-ls-write-at-rptr", TOP, "tf_ls_ram_r[tf_wptr_r[1]]", "tf_ls_ram_r[tf_rptr_r[1]]",
  "srp_top", "RUN_ARGS=storage"),
 ("tf-tk-push-dropped-when-both", TOP, "    if (tf_push_w[0]) begin\n      tf_tk_ram_r",
  "    if (tf_push_w[0] && !tf_push_w[1]) begin\n      tf_tk_ram_r", "srp_top", "RUN_ARGS=storage"),
 ("wtsp-mfs-mif-swapped-on-write", TK, "{gate_max_frame_i, gate_max_interval_i,",
  "{gate_max_interval_i, gate_max_frame_i,", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wid-vlan-slice-off-by-one", TK, "wval_w[159:144] = {4'd0, wid_w[11:0]};",
  "wval_w[159:144] = {4'd0, wid_w[12:1]};", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wid-ram-write-at-walk-source", TK, "wid_r[gate_src_i] <=", "wid_r[wsrc_r] <=",
  "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wsid-ram-read-at-control-sink", LS, "assign wsid_w = wsid_r[wsrc_r];",
  "assign wsid_w = wsid_r[ctl_sink_i];", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wsid-ram-write-ignores-ready", LS, "if (rst_n && ctl_acc_w && ctl_settle_i) begin",
  "if (rst_n && ctl_valid_i && ctl_settle_i) begin", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wtsp-write-ignores-ready", TK, "assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
  "assign gate_open_acc_w = rst_n && gate_valid_i && gate_open_i;", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("wtsp-write-during-reset", TK, "assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
  "assign gate_open_acc_w = gate_acc_w && gate_open_i;", "srp_stream_fsms", "RUN_ARGS=walk"),
 ("slope-cand-reads-neighbour", AD, "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r]};",
  "assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[(aidx_r == '0) ? SRC_W_C'(N_SOURCES_P - 1) : aidx_r - SRC_W_C'(1)]};",
  "srp_admission", ""),
 ("slope-store-skips-last-source", AD, "    if (rst_n) begin\n      slope_q_r[cidx_q2_r]",
  "    if (rst_n && (32'(cidx_q2_r) != N_SOURCES_P - 1)) begin\n      slope_q_r[cidx_q2_r]",
  "srp_admission", ""),
]

def one(p, head, scratch, rec):
    label, f, old, new, suite, args = p
    tree = scratch / label
    if tree.exists(): shutil.rmtree(tree)
    tree.mkdir(parents=True)
    shutil.copytree(head / "hdl", tree / "hdl")
    shutil.copytree(head / "tb" / suite, tree / "tb" / suite,
                    ignore=shutil.ignore_patterns("obj_*"))
    if (head / "tb" / "common").exists():
        shutil.copytree(head / "tb" / "common", tree / "tb" / "common")
    src = (tree / f).read_text()
    if src.count(old) != 1:
        return label, suite, "EDIT-NOT-UNIQUE", src.count(old), 0
    (tree / f).write_text(src.replace(old, new))
    env = dict(os.environ, VJ="1")
    vl = str(Path(__file__).resolve().parent / "verilator-j.sh")
    cmd = ["make", "-C", str(tree / "tb" / suite), "VERILATOR=" + vl] + ([args] if args else [])
    with open(rec / f"probe-{label}.log", "w") as log:
        rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, env=env).returncode
    text = (rec / f"probe-{label}.log").read_text()
    fails = [l for l in text.splitlines() if "FAIL" in l and "0 FAIL" not in l]
    built = "checks" in text or "PASS" in text
    verdict = "CAUGHT" if (rc != 0 and fails and built) else ("SURVIVED" if rc == 0 else "UNPROVEN")
    return label, suite, verdict, rc, len(fails)

def main():
    head, scratch, rec = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    jobs = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[4] == "--jobs" else 4
    scratch.mkdir(parents=True, exist_ok=True); rec.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(lambda p: one(p, head, scratch, rec), PROBES))
    for r in res: print("%-32s %-16s %-16s rc=%s fail-lines=%s" % r)
    return 0
if __name__ == "__main__":
    sys.exit(main())

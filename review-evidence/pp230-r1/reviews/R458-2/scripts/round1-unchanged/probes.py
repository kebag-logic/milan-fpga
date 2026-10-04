#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R458-1 disposable fault probes for milan-fpga #230 / processor PR #154.

Each probe is one textual edit of the HEAD RTL. For each probe this script
copies the head tree's hdl/ and the SRP benches into <work>/<probe>/, applies
the edit (it must match exactly once), and runs:
  - the committed suites that build the edited file (tb/srp_top,
    tb/srp_stream_fsms, tb/srp_admission all shapes), recording rc;
  - the reviewer's module-level lockstep (ls_fsm) at N = 1, 2, 3, 9 for
    talker/listener/admission probes, 300,000 cycles x 3 seeds each;
  - the reviewer's top-level lockstep (committed tb/srp_top stimulus through
    base and head KL_srp_top) for KL_srp_top probes.
A probe is CAUGHT by a committed suite when that suite's rc != 0.

usage: probes.py <base_tree> <head_tree> <work> <verilator> [probe ...]
"""
import concurrent.futures as cf
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASE = None

TK = "hdl/srp/KL_srp_talker_fsm.sv"
LS = "hdl/srp/KL_srp_listener_fsm.sv"
AD = "hdl/srp/KL_srp_admission.sv"
TOP = "hdl/srp/KL_srp_top.sv"

PROBES = {
    # timer-arm FIFOs (lever 2)
    "tf-heads-swapped": (TOP, [
        ("tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];", "tf_q_r[0] <= tf_ls_ram_r[tf_rptr_r[0]];"),
        ("tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];", "tf_q_r[1] <= tf_tk_ram_r[tf_rptr_r[1]];")]),
    "tf-ls-written-at-tk-pointer": (TOP, [
        ("tf_ls_ram_r[tf_wptr_r[1]]", "tf_ls_ram_r[tf_wptr_r[0]]")]),
    "tf-tk-head-read-ahead": (TOP, [
        ("tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0]];", "tf_q_r[0] <= tf_tk_ram_r[tf_rptr_r[0] + 5'd1];")]),
    "tf-full-guard-31": (TOP, [
        ("assign tf_push_w[0] = tk_arm_v_w && (tf_cnt_r[0] != 6'(TFD_C));",
         "assign tf_push_w[0] = tk_arm_v_w && (tf_cnt_r[0] != 6'(TFD_C - 1));")]),
    # talker walk record (lever 4 storage)
    "wtsp-read-at-gate-source": (TK, [
        ("assign wtsp_w = wtsp_r[wsrc_r];", "assign wtsp_w = wtsp_r[gate_src_i];")]),
    "wtsp-first-open-only": (TK, [
        ("    if (gate_open_acc_w) begin\n      wtsp_r[gate_src_i]",
         "    if (gate_open_acc_w && !rec_valid_r[gate_src_i]) begin\n      wtsp_r[gate_src_i]")]),
    "wtsp-latency-shifted": (TK, [
        ("wval_w[103:72]  = wtsp_w[31:0];", "wval_w[103:72]  = {wtsp_w[30:0], 1'b0};")]),
    "wtsp-rank-dropped": (TK, [
        ("wval_w[111:104] = {wtsp_w[35:32], 4'd0};", "wval_w[111:104] = {wtsp_w[35:33], 1'b0, 4'd0};")]),
    "wid-ram-first-open-only": (TK, [
        ("      if (gate_open_acc_w) begin\n        wid_r[gate_src_i]",
         "      if (gate_open_acc_w && !rec_valid_r[gate_src_i]) begin\n        wid_r[gate_src_i]")]),
    "wid-ram-read-at-gate-source": (TK, [
        ("assign wid_w = wid_r[wsrc_r];", "assign wid_w = wid_r[gate_src_i];")]),
    "wid-flops-da-of-gate-source": (TK, [
        ("assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
         "assign wid_w = {sid_r[wsrc_r], da_r[gate_src_i], vid_r[wsrc_r]};")]),
    "wid-flops-sid-of-source-0": (TK, [
        ("assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
         "assign wid_w = {sid_r[0], da_r[wsrc_r], vid_r[wsrc_r]};")]),
    # listener walk stream_id
    "wsid-ram-first-settle-only": (LS, [
        ("if (rst_n && ctl_acc_w && ctl_settle_i) begin",
         "if (rst_n && ctl_acc_w && ctl_settle_i && !rec_valid_r[ctl_sink_i]) begin")]),
    "wsid-ram-written-on-teardown": (LS, [
        ("if (rst_n && ctl_acc_w && ctl_settle_i) begin", "if (rst_n && ctl_acc_w) begin")]),
    "wsid-flops-of-control-sink": (LS, [
        ("assign wsid_w = sid_r[wsrc_r];", "assign wsid_w = sid_r[ctl_sink_i];")]),
    # admission slopes
    "slope-stored-at-stage-2-index": (AD, [
        ("slope_q_r[cidx_q2_r] <=", "slope_q_r[cidx_q1_r] <=")]),
    "slope-stored-at-source-0": (AD, [
        ("slope_q_r[cidx_q2_r] <=", "slope_q_r[0] <=")]),
}

SUITES_FOR = {TOP: ["srp_top"], TK: ["srp_top", "srp_stream_fsms"],
              LS: ["srp_top", "srp_stream_fsms"], AD: ["srp_top", "srp_admission"]}


def run(cmd, cwd, log, env=None):
    with open(log, "w") as fh:
        return subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT,
                              env=env, check=False).returncode


def prep(head, work, name):
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(head / "hdl", d / "hdl")
    for t in ("common", "srp_top", "srp_stream_fsms", "srp_admission"):
        shutil.copytree(head / "tb" / t, d / "tb" / t,
                        ignore=shutil.ignore_patterns("obj_*"))
    f, edits = PROBES[name]
    p = d / f
    s = p.read_text()
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"{name}: anchor matched {n} times: {old!r}")
        s = s.replace(old, new)
    p.write_text(s)
    if f != TOP:
        run([sys.executable, str(HERE / "gen_top_lockstep.py"), str(BASE), str(d), str(d / "gen")],
            d, d / "gen.log")
    return d, f


def task_suite(d, suite, vj4):
    log = d / f"suite-{suite}.log"
    rc = run(["make", f"VERILATOR={vj4}"], d / "tb" / suite, log)
    return rc


def task_fsm(base, d, n, vj4, seeds=(1, 2, 3), cycles=300000):
    w = d / f"ls_fsm{n}"
    gen = d / "gen"
    env = dict(os.environ, VERILATOR=vj4)
    rc = run([str(HERE / "build_fsm_lockstep.sh"), str(gen / "srp_ref"), str(gen / "srp_new"),
              str(d), str(n), str(w)], d, d / f"build-fsm{n}.log", env)
    if rc:
        return f"build-rc{rc}"
    total = 0
    for sd in seeds:
        out = subprocess.run([str(w / "obj_dir/Vls_fsm"), str(cycles), str(sd)],
                             capture_output=True, text=True, check=False).stdout
        (d / f"ls_fsm{n}-seed{sd}.log").write_text(out)
        m = re.search(r"mis_tk=(\d+) mis_ls=(\d+) mis_ad=(\d+)", out)
        total += sum(int(x) for x in m.groups()) if m else 10**9
    return total


def task_top(base, d, vj4):
    w = d / "ls_top"
    env = dict(os.environ, VERILATOR=vj4)
    rc = run([str(HERE / "build_top_lockstep.sh"), str(base), str(d), str(w)], d,
             d / "build-top.log", env)
    if rc:
        return f"build-rc{rc}"
    rc = run([str(w / "obj_dir/Vsrp_top_sim")], w, d / "ls_top.log", dict(os.environ, LS_SEED="7"))
    txt = (d / "ls_top.log").read_text()
    m = re.search(r"mismatching_out=(\d+) mismatching_int=(\d+)", txt)
    return f"{m.group(1)}/{m.group(2)} (bench rc {rc})" if m else f"no-summary rc {rc}"


def main():
    global BASE
    base, head, work = (pathlib.Path(a).resolve() for a in sys.argv[1:4])
    BASE = base
    vj4 = sys.argv[4]
    names = sys.argv[5:] or list(PROBES)
    work.mkdir(parents=True, exist_ok=True)
    dirs = {}
    for n in names:
        dirs[n] = prep(head, work, n)
    futs = {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for n, (d, f) in dirs.items():
            for s in SUITES_FOR[f]:
                futs[ex.submit(task_suite, d, s, vj4)] = (n, s)
            if f == TOP:
                futs[ex.submit(task_top, base, d, vj4)] = (n, "lockstep-top")
            else:
                for k in (1, 2, 3, 9):
                    futs[ex.submit(task_fsm, base, d, k, vj4)] = (n, f"lockstep-N{k}")
        res = {}
        for fu in cf.as_completed(futs):
            res[futs[fu]] = fu.result()
    lines = ["probe\trun\tresult"]
    for (n, r), v in sorted(res.items()):
        lines.append(f"{n}\t{r}\t{v}")
    (work / "probe_results.tsv").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

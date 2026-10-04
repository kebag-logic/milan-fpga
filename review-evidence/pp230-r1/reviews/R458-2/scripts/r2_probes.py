#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R458-2 disposable probes for milan-fpga #230 / processor PR #154.

Each probe is one textual edit of the head tree (RTL or the test wrap). For
each probe this script copies the head's hdl/ and the SRP benches into
<work>/<probe>/, applies the edit (each anchor must match exactly once), and
runs the committed make targets named for it, recording rc, the tally lines
and the FAIL lines (with their [sources/sinks] suffix).

What the probes ask:
  tm-enum-swapped        RTL-neutral: KL_srp_top's issue-state encoding swapped
                         (TM_SEL = 1, TM_POP = 0). The engine's behaviour is
                         unchanged (the 2,200-check suite must still pass), but
                         the wrap names TM_SEL as 1'b0: does the held arm fail
                         loudly, or pass silently?
  wrap-force-dropped     the wrap's force removed (tm_stall_i does nothing):
                         is the held arm non-vacuous?
  tm-sel-skips-full-tk   a full-specific selection defect (the talker FIFO is
                         never selected while it holds 32 words): does the held
                         arm, which drains from full unforced, catch it?
  tm-sel-skips-full-ls   the same for the listener FIFO.
  wid-flops-sid-of-gate-source / wid-flops-vid-of-gate-source
                         the talker flop arm reading the 64-bit stream_id or the
                         12-bit VLAN at the idle gate face: how far the 64-bit
                         packed-element aliasing reaches at 1/1.

usage: r2_probes.py <head_tree> <work> [probe ...]
VERILATOR must name the pinned tool (or a wrapper for it).
"""
import concurrent.futures as cf
import os
import pathlib
import re
import shutil
import subprocess
import sys

TOP = "hdl/srp/KL_srp_top.sv"
TK = "hdl/srp/KL_srp_talker_fsm.sv"
WRAP = "tb/srp_top/srp_store_wrap.sv"

PROBES = {
    "tm-enum-swapped": (TOP, [
        ("    TM_SEL = 1'b0,   // pick a source", "    TM_SEL = 1'b1,   // pick a source"),
        ("    TM_POP = 1'b1    // issue the FIFO word", "    TM_POP = 1'b0    // issue the FIFO word")],
        [("srp_top", "storage"), ("srp_top", "run")]),
    "wrap-force-dropped": (WRAP, [
        ("    if (tm_stall_i) force u_dut.tm_st_r = type(u_dut.tm_st_r)'(TB_TM_SEL_C);\n"
         "    else release u_dut.tm_st_r;\n",
         "    if (tm_stall_i) ;\n")],
        [("srp_top", "storage")]),
    "tm-sel-skips-full-tk": (TOP, [
        ("if ((tf_cnt_r[0] != 6'd0) && (!tm_rr_r || (tf_cnt_r[1] == 6'd0)))",
         "if ((tf_cnt_r[0] != 6'd0) && (tf_cnt_r[0] != 6'd32) && (!tm_rr_r || (tf_cnt_r[1] == 6'd0)))")],
        [("srp_top", "storage")]),
    "tm-sel-skips-full-ls": (TOP, [
        ("end else if (tf_cnt_r[1] != 6'd0) begin\n            tm_sel_r <= 1'b1;",
         "end else if ((tf_cnt_r[1] != 6'd0) && (tf_cnt_r[1] != 6'd32)) begin\n            tm_sel_r <= 1'b1;")],
        [("srp_top", "storage")]),
    "wid-flops-sid-of-gate-source": (TK, [
        ("assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
         "assign wid_w = {sid_r[gate_src_i], da_r[wsrc_r], vid_r[wsrc_r]};")],
        [("srp_stream_fsms", "walk:1x1"), ("srp_stream_fsms", "walk:2x2")]),
    "wid-flops-vid-of-gate-source": (TK, [
        ("assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[wsrc_r]};",
         "assign wid_w = {sid_r[wsrc_r], da_r[wsrc_r], vid_r[gate_src_i]};")],
        [("srp_stream_fsms", "walk:1x1"), ("srp_stream_fsms", "walk:2x2")]),
}


def prep(head, work, name):
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(head / "hdl", d / "hdl")
    for t in ("common", "srp_top", "srp_stream_fsms"):
        shutil.copytree(head / "tb" / t, d / "tb" / t, ignore=shutil.ignore_patterns("obj_*"))
    f, edits, _ = PROBES[name]
    p = d / f
    s = p.read_text()
    for old, new in edits:
        n = s.count(old)
        if n != 1:
            raise SystemExit(f"{name}: anchor matched {n} times: {old!r}")
        s = s.replace(old, new)
    p.write_text(s)
    return d


def run_target(d, suite, target):
    """target: 'storage' / 'walk' (RUN_ARGS group), 'run' (the suite alone) or 'walk:<shape>'."""
    if target.startswith("walk:"):
        args = ["make", "walk", "SHAPE=" + target.split(":", 1)[1]]
    elif target == "run":
        args = ["make", "run"]
    else:
        args = ["make", "RUN_ARGS=" + target]
    args.append("VERILATOR=" + os.environ["VERILATOR"])
    log = d / f"{suite}-{target.replace(':', '_')}.log"
    with open(log, "w") as fh:
        rc = subprocess.run(args, cwd=d / "tb" / suite, stdout=fh, stderr=subprocess.STDOUT,
                            check=False).returncode
    txt = log.read_text()
    tallies = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", txt)
    fails = [ln for ln in txt.splitlines() if ln.startswith("FAIL:")]
    return rc, tallies, fails


def main():
    head, work = (pathlib.Path(a).resolve() for a in sys.argv[1:3])
    names = sys.argv[3:] or list(PROBES)
    work.mkdir(parents=True, exist_ok=True)
    jobs = []
    for n in names:
        d = prep(head, work, n)
        for suite, target in PROBES[n][2]:
            jobs.append((n, d, suite, target))
    out = []
    with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("R2_JOBS", "4"))) as ex:
        futs = {ex.submit(run_target, d, s, t): (n, s, t) for n, d, s, t in jobs}
        res = {futs[f]: f.result() for f in cf.as_completed(futs)}
    for key in sorted(res):
        n, s, t = key
        rc, tallies, fails = res[key]
        out.append(f"{n}\t{s} {t}\trc={rc}\t{' | '.join(tallies)}")
        for ln in fails[:12]:
            out.append(f"    {ln}")
        if len(fails) > 12:
            out.append(f"    ... {len(fails) - 12} more FAIL lines")
    text = "\n".join(out) + "\n"
    (work / "r2_probe_results.txt").write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()

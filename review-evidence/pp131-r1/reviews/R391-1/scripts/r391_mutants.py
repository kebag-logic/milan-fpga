#!/usr/bin/env python3
"""Reviewer mutation probe: plant one textual mutant per scratch copy of the
processor tree, build tb/pp_top and run its D3 section (--d3-only).
KILLED = build ok and the run exits non-zero; SURVIVED = build ok, exit 0.
Usage: r391_mutants.py --tree <clean tree> --scratch <dir> --verilator-dir <dir> [--jobs N]
"""
import argparse, concurrent.futures as cf, os, re, shutil, subprocess, sys

W = "hdl/aecp/KL_aecp_nvm_writer.sv"
MUTANTS = {
    # the rate list walk never advances past its first lane
    "rate_walk_stuck_on_first_lane": (W,
        "lane_off_r <= SSR_LIST_OFF_C + (16'(walk_next_w) << 2);",
        "lane_off_r <= SSR_LIST_OFF_C;"),
    # the eight-entry bound of the SET program's walk is dropped
    "rate_walk_unbounded": (W,
        "lane_refuse_w = (walk_next_w == SSR_WALK_MAX_C)\n                      || (rcount_r == 16'(walk_next_w));",
        "lane_refuse_w = (rcount_r == 16'(walk_next_w));"),
    # a pass-1 deadline no longer abandons the granted READ to the drain
    "pass1_read_not_drained": (W,
        "assign m_abort_o  = expire_w && (ws_r == W_RD);",
        "assign m_abort_o  = expire_w && (ws_r == W_RD) && !pass_r;"),
    # the format judge's wait is not watched by the deadline
    "judge_wait_unwatched": (W,
        "W_JUDGE: stall_w = jd_wait_i;",
        "W_JUDGE: stall_w = 1'b0;"),
    # cross-check of the other public review's F3 items 2-4
    "backoff_holds_dispatch": (W,
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;",
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w || (ss_r == S_BACKOFF);"),
    "disagree_whole_then_blank_only": (W,
        "&& (rd_whole_w != whole0_r[rec_r]);",
        "&& (!rd_whole_w && whole0_r[rec_r]);"),
    "rollback_strobe_one_cycle": (W,
        "if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;",
        "if (!desc_debt_i) ws_r <= W_RELOC;"),
}

def run(name, tree, scratch, vdir):
    path, old, new = MUTANTS[name]
    d = os.path.join(scratch, "mut-" + name)
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(tree, d, symlinks=True,
                    ignore=shutil.ignore_patterns("obj_dir", "obj_vid"))
    f = os.path.join(d, path)
    src = open(f).read()
    if src.count(old) != 1:
        return name, "REFUSED (anchor count %d)" % src.count(old), None, None
    open(f, "w").write(src.replace(old, new))
    env = dict(os.environ, PATH=vdir + os.pathsep + os.environ["PATH"])
    tb = os.path.join(d, "tb/pp_top")
    b = subprocess.run(["make", "gsi-build"], cwd=tb, env=env,
                       capture_output=True, text=True)
    open(os.path.join(d, "build.log"), "w").write(b.stdout + b.stderr)
    if b.returncode != 0:
        return name, "BUILD-FAIL", b.returncode, None
    r = subprocess.run(["./obj_dir/Vpp_top_sim", "--d3-only"], cwd=tb, env=env,
                       capture_output=True, text=True, timeout=3000)
    open(os.path.join(d, "run.log"), "w").write(r.stdout + r.stderr)
    fails = [l for l in r.stdout.splitlines() if "FAIL" in l][:3]
    tally = [l for l in r.stdout.splitlines() if l.startswith("D3:")]
    verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    return name, verdict, r.returncode, (tally[-1] if tally else "") + " | " + " || ".join(fails)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--verilator-dir", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    names = a.only or list(MUTANTS)
    with cf.ThreadPoolExecutor(max_workers=min(a.jobs, 8)) as ex:
        futs = [ex.submit(run, n, a.tree, a.scratch, a.verilator_dir) for n in names]
        for fu in cf.as_completed(futs):
            n, v, rc, info = fu.result()
            print("%-34s %-10s rc=%s %s" % (n, v, rc, info or ""), flush=True)

if __name__ == "__main__":
    sys.exit(main())

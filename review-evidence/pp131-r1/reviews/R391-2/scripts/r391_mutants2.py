#!/usr/bin/env python3
"""Reviewer mutation probe (R391-1 set re-run at R391-2, plus R391-2 additions):
plant one textual mutant per scratch copy of the processor tree, build
tb/pp_top and run its D3 section (--d3-only), or the full pp_top run with --full.
KILLED = build ok and the run exits non-zero; SURVIVED = build ok, exit 0.
Usage: r391_mutants.py --tree <clean tree> --scratch <dir> --verilator-dir <dir> [--jobs N]
"""
import argparse, concurrent.futures as cf, os, re, shutil, subprocess, sys

W = "hdl/aecp/KL_aecp_nvm_writer.sv"
T = "hdl/top/protocol_processor_top.sv"
V = "hdl/packet_engine/KL_pp_rx_validator.sv"
HOLD = "  assign aecp_rx_hold_w = !d3_done_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);"
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
    # ---- R391-2 additions: the aggregate (DR3a) ----
    # the bound may fire with an event in hand (a grant, a byte, an answer)
    "agg_fires_with_event_in_hand": (W,
        "  assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1))\n                        && (stall_w || !wait_w);",
        "  assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1));"),
    # the aggregate keeps running after the terminal
    "agg_not_stopped_at_terminal": (W,
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r && !done_r && !closed_r;",
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r;"),
    # the aggregate fires more than once
    "agg_not_one_shot": (W,
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r && !done_r && !closed_r;",
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !done_r && !closed_r;"),
    # ---- R391-2 additions: the AECP hold admission ----
    "hold_admits_two": (T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && ((aecp_rx_res_r > 'd1) || (aecp_rx_res_r != '0 && aecp_rx_in_w));"),
    "hold_released_in_closed": (T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && !d3_closed_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);"),
    "held_gate_drops_every_subtype": (V,
        "                       && (rx_data_i == SUB_AECP_C) && (da_own_r | da_mcast_r);",
        "                       && (da_own_r | da_mcast_r);"),
    "resident_counts_acmp": (T,
        "                         && (v_hdr_protocol_w != 3'(PP_PROTO_ACMP))\n",
        ""),
    "resident_never_returned": (T,
        "  assign aecp_rx_out_w = {1'b0, aecp_rxs_free_w} + {1'b0, aecp_rxs_free_i};",
        "  assign aecp_rx_out_w = 2'd0;"),
}

FULL = False

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
    args = [] if FULL else ["--d3-only"]
    r = subprocess.run(["./obj_dir/Vpp_top_sim"] + args, cwd=tb, env=env,
                       capture_output=True, text=True, timeout=6000)
    open(os.path.join(d, "run.log"), "w").write(r.stdout + r.stderr)
    fails = [l for l in r.stdout.splitlines() if "FAIL" in l][:3]
    tally = [l for l in r.stdout.splitlines() if l.startswith("D3:") or " checks: " in l or "checks," in l]
    verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    return name, verdict, r.returncode, (tally[-1] if tally else "") + " | " + " || ".join(fails)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--verilator-dir", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    global FULL
    FULL = a.full
    names = a.only or list(MUTANTS)
    with cf.ThreadPoolExecutor(max_workers=min(a.jobs, 8)) as ex:
        futs = [ex.submit(run, n, a.tree, a.scratch, a.verilator_dir) for n in names]
        for fu in cf.as_completed(futs):
            n, v, rc, info = fu.result()
            print("%-34s %-10s rc=%s %s" % (n, v, rc, info or ""), flush=True)

if __name__ == "__main__":
    sys.exit(main())

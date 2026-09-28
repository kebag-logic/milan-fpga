#!/usr/bin/env python3
"""R367-3 disposable probes for PR #603 (issue #602), exact head 6b2ebd1c.

Usage: python3 probe_r367_3.py <tree> <old_harness_tree> <scratch> <receipts> [--only NAME ...]

<tree> is a disposable copy of the candidate at 6b2ebd1c (with git metadata so
the suite Makefile can derive the processor source list). <old_harness_tree>
is the same copy with tb/verilator/milan_dp/sim_main.cpp taken from 471892a9
(the round-2 harness), used only by the OH* probes. Nothing in either tree is
edited by this script: mutants are written under <scratch>/mutants and passed
through the suite's own DP_SRC / MCR_SRC make variables. PATH must name the
pinned Verilator 5.050. Each probe writes <receipts>/<name>.log and one
summary line to <receipts>/summary.tsv: name, leg, harness, rc, checks,
failures, failed check names. At most 8 runs execute in parallel.
"""
import argparse
import concurrent.futures as cf
import re
import subprocess
import sys
from pathlib import Path

RESTART = "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);"
REBASE = "  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;\n"
MCR_RESET = "      tgt_r <= '0;\n      mr_o  <= '0;"


def delayed_adjtime(n):
    """An adjtime-caused restart request landing n cycles after the adjtime
    pulse: a reviewer-written down-counter (independent of the executor's
    shift-register and counter controls)."""
    decl = (f"  logic [19:0] r367_dly_r;\n"
            f"  always_ff @(posedge axis_clk) begin : r367_dly\n"
            f"    if (!axis_resetn) r367_dly_r <= '0;\n"
            f"    else if (eff_ptp_adjust_w) r367_dly_r <= 20'd{n};\n"
            f"    else if (r367_dly_r != 20'd0) r367_dly_r <= r367_dly_r - 20'd1;\n"
            f"  end : r367_dly\n")
    return [(REBASE, decl + REBASE),
            (RESTART, RESTART[:-1] + " | (r367_dly_r == 20'd1);")]


# name, leg, harness ('new' | 'old'), source key, [(anchor, replacement), ...]
PROBES = [
    ("O0_clean", "optoff", "new", None, []),
    ("O1_adjtime_only", "optoff", "new", "dp", [(RESTART, RESTART[:-1] + " | eff_ptp_adjust_w;")]),
    ("O2_settime_only", "optoff", "new", "dp", [(RESTART, RESTART[:-1] + " | cfg_ptp_cmd_load;")]),
    ("O3_both", "optoff", "new", "dp", [(RESTART, RESTART[:-1] + " | media_rebase_p_w;")]),
    # event-relative witness: the pre-event level is 1, no event changes it
    ("O4_mr_resets_high", "optoff", "new", "mcr",
     [(MCR_RESET, "      tgt_r <= '1;\n      mr_o  <= '1;")]),
    ("O5_adjtime_delay16", "optoff", "new", "dp", delayed_adjtime(16)),
    ("O6_adjtime_delay256", "optoff", "new", "dp", delayed_adjtime(256)),
    ("O7_adjtime_delay4096", "optoff", "new", "dp", delayed_adjtime(4096)),
    ("O8_adjtime_delay65536", "optoff", "new", "dp", delayed_adjtime(65536)),
    # the round-2 harness against the same delayed causes: shows what the fix adds
    ("OH0_clean_oldharness", "optoff", "old", None, []),
    ("OH5_delay16_oldharness", "optoff", "old", "dp", delayed_adjtime(16)),
    ("OH6_delay256_oldharness", "optoff", "old", "dp", delayed_adjtime(256)),
    ("G0_clean", "gmstep", "new", None, []),
    ("G1_rebase_restored", "gmstep", "new", "dp", [(RESTART, RESTART[:-1] + " | media_rebase_p_w;")]),
    ("G2_suppress_on_rebase", "gmstep", "new", "dp", [(RESTART, RESTART[:-1] + " & ~media_rebase_p_w;")]),
    ("G3_crf_propagation_removed", "gmstep", "new", "dp",
     [(RESTART, "                          & (tkd_crflk_q_r & ~crf_locked_w);")]),
    ("G4_settime_restored", "gmstep", "new", "dp", [(RESTART, RESTART[:-1] + " | cfg_ptp_cmd_load;")]),
]

LEG = {
    "optoff": ("option-off-build", "OPTOFF_MDIR", "Vmilan_dp_sim", False),
    "gmstep": ("gmstep-build", "GMSTEP_MDIR", "Vmilan_dp_gmstep", True),
}
SRC = {"dp": ("DP_SRC", "hdl/milan/milan_datapath.sv"),
       "mcr": ("MCR_SRC", "hdl/ieee1722/avtp/KL_media_clock_restart.sv")}


def build(trees, scratch, name, leg, harness, key, plants):
    tree = trees[harness]
    target, mvar, exe, _ = LEG[leg]
    mdir = scratch / f"obj_{name}"
    cmd = ["make", "-s", "-C", str(tree / "tb/verilator/milan_dp"), target,
           f"{mvar}={mdir}", "VERILATOR_JOBS=8"]
    if key:
        var, rel = SRC[key]
        text = (tree / rel).read_text()
        for anchor, repl in plants:
            if text.count(anchor) != 1:
                raise SystemExit(f"{name}: anchor count {text.count(anchor)}")
            text = text.replace(anchor, repl)
        planted = scratch / "mutants" / f"{name}_{Path(rel).name}"
        planted.parent.mkdir(parents=True, exist_ok=True)
        planted.write_text(text)
        cmd.append(f"{var}={planted}")
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if out.returncode != 0 or not (mdir / exe).is_file():
        raise SystemExit(f"{name}: build failed\n{out.stdout[-2000:]}{out.stderr[-2000:]}")
    return mdir / exe


def run(tree, exe, leg):
    args = [str(exe)] + ([str(exe.parent / "aemi.bin")] if LEG[leg][3] else [])
    out = subprocess.run(args, cwd=str(tree / "tb/verilator/milan_dp"),
                         capture_output=True, text=True, timeout=1800)
    return out.returncode, out.stdout + out.stderr


def summarize(name, leg, harness, rc, log):
    fails = [l.strip()[len("[FAIL]"):].split(" got=")[0].strip()
             for l in log.splitlines() if l.strip().startswith("[FAIL]")]
    m = re.findall(r"checks:\s*(\d+)\s+failures:\s*(\d+)", log)
    if not m:
        m = re.findall(r"(\d+) checks, (\d+) failures", log)
    if not m:
        m = re.findall(r"(\d+)/(\d+) checks? (?:passed|PASS)", log)
    checks, nfail = (m[-1] if m else ("?", str(len(fails))))
    return f"{name}\t{leg}\t{harness}\t{rc}\t{checks}\t{nfail}\t{' | '.join(fails)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("old_tree", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("receipts", type=Path)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.receipts.mkdir(parents=True, exist_ok=True)
    trees = {"new": a.tree, "old": a.old_tree}
    sel = [p for p in PROBES if not a.only or p[0] in a.only]
    exes = {p[0]: build(trees, a.scratch, *p) for p in sel}

    def one(p):
        rc, log = run(trees[p[2]], exes[p[0]], p[1])
        (a.receipts / f"{p[0]}.log").write_text(log)
        return summarize(p[0], p[1], p[2], rc, log)
    with cf.ThreadPoolExecutor(8) as pool:
        rows = list(pool.map(one, sel))
    out = a.receipts / ("summary.tsv" if not a.only else "summary_" + "_".join(a.only) + ".tsv")
    out.write_text("\n".join(rows) + "\n")
    print("\n".join(rows))


if __name__ == "__main__":
    sys.exit(main())

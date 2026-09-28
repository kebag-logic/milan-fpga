#!/usr/bin/env python3
"""R367-2 disposable probes for PR #603 (issue #602), exact head 471892a9.

Usage: python3 probe_r367_2.py <tree> <scratch> <receipts> [--only NAME ...]

<tree> is a disposable copy of the candidate (with git metadata so the suite
Makefile can derive the processor source list); nothing in it is edited, the
mutants are written under <scratch>/mutants and passed through the suite's own
DP_SRC / MCR_SRC make variables. PATH must name the pinned Verilator 5.050.
Each probe writes <receipts>/<name>.log and one summary line to
<receipts>/summary.tsv: name, leg, rc, checks, failures, failed check names.
"""
import argparse
import concurrent.futures as cf
import re
import subprocess
import sys
from pathlib import Path

RESTART = "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);"
MCR_RESET = "      tgt_r <= '0;\n      mr_o  <= '0;"

# name, leg, source key, anchor, replacement
PROBES = [
    ("O0_clean", "optoff", None, None, None),
    ("O1_adjtime_only", "optoff", "dp", RESTART, RESTART[:-1] + " | eff_ptp_adjust_w;"),
    ("O2_settime_only", "optoff", "dp", RESTART, RESTART[:-1] + " | cfg_ptp_cmd_load;"),
    ("O3_both", "optoff", "dp", RESTART, RESTART[:-1] + " | media_rebase_p_w;"),
    # event-relative witness: the pre-event level is 1, no event changes it
    ("O4_mr_resets_high", "optoff", "mcr", MCR_RESET,
     "      tgt_r <= '1;\n      mr_o  <= '1;"),
    ("G0_clean", "gmstep", None, None, None),
    ("G1_rebase_restored", "gmstep", "dp", RESTART, RESTART[:-1] + " | media_rebase_p_w;"),
    ("G2_suppress_on_rebase", "gmstep", "dp", RESTART, RESTART[:-1] + " & ~media_rebase_p_w;"),
    ("G3_crf_propagation_removed", "gmstep", "dp", RESTART,
     "                          & (tkd_crflk_q_r & ~crf_locked_w);"),
    ("G4_settime_restored", "gmstep", "dp", RESTART, RESTART[:-1] + " | cfg_ptp_cmd_load;"),
]

LEG = {
    "optoff": ("option-off-build", "OPTOFF_MDIR", "Vmilan_dp_sim", False),
    "gmstep": ("gmstep-build", "GMSTEP_MDIR", "Vmilan_dp_gmstep", True),
}
SRC = {"dp": ("DP_SRC", "hdl/milan/milan_datapath.sv"),
       "mcr": ("MCR_SRC", "hdl/ieee1722/avtp/KL_media_clock_restart.sv")}


def build(tree, scratch, name, leg, key, anchor, repl):
    target, mvar, exe, _ = LEG[leg]
    mdir = scratch / f"obj_{name}"
    cmd = ["make", "-s", "-C", str(tree / "tb/verilator/milan_dp"), target,
           f"{mvar}={mdir}", "VERILATOR_JOBS=4"]
    if key:
        var, rel = SRC[key]
        text = (tree / rel).read_text()
        if text.count(anchor) != 1:
            raise SystemExit(f"{name}: anchor count {text.count(anchor)}")
        planted = scratch / "mutants" / f"{name}_{Path(rel).name}"
        planted.parent.mkdir(parents=True, exist_ok=True)
        planted.write_text(text.replace(anchor, repl))
        cmd.append(f"{var}={planted}")
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if out.returncode != 0 or not (mdir / exe).is_file():
        raise SystemExit(f"{name}: build failed\n{out.stdout[-2000:]}{out.stderr[-2000:]}")
    return mdir / exe


def run(tree, exe, leg, extra=()):
    args = [str(exe)] + ([str(exe.parent / "aemi.bin")] if LEG[leg][3] else []) + list(extra)
    out = subprocess.run(args, cwd=str(tree / "tb/verilator/milan_dp"),
                         capture_output=True, text=True, timeout=900)
    return out.returncode, out.stdout + out.stderr


def summarize(name, leg, rc, log):
    fails = [l.strip()[len("[FAIL]"):].split(" got=")[0].strip()
             for l in log.splitlines() if l.strip().startswith("[FAIL]")]
    m = re.findall(r"checks:\s*(\d+)\s+failures:\s*(\d+)", log)
    if not m:
        m = re.findall(r"(\d+) checks, (\d+) failures", log)
    checks, nfail = (m[-1] if m else ("?", str(len(fails))))
    return f"{name}\t{leg}\t{rc}\t{checks}\t{nfail}\t{' | '.join(fails)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("receipts", type=Path)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--feed-sweep", action="store_true",
                    help="run the clean gmstep binary at GMSTEP_FEED_DELAY 0..41")
    a = ap.parse_args()
    a.receipts.mkdir(parents=True, exist_ok=True)
    rows = []
    if a.feed_sweep:
        exe = build(a.tree, a.scratch, "G0_clean", "gmstep", None, None, None)

        def one(d):
            rc, log = run(a.tree, exe, "gmstep", [str(d)])
            (a.receipts / f"feed_{d:02d}.log").write_text(log)
            ov = [int(x) for x in re.findall(r"COINCIDENT: delay \d+, overlap (\d+)", log)]
            return summarize(f"feed_{d:02d}", "gmstep", rc, log) + f"\toverlap_trials={sum(1 for x in ov if x)}"
        with cf.ThreadPoolExecutor(8) as pool:
            rows = list(pool.map(one, range(42)))
        out = a.receipts / "feed_sweep.tsv"
    else:
        sel = [p for p in PROBES if not a.only or p[0] in a.only]
        exes = {p[0]: build(a.tree, a.scratch, *p) for p in sel}

        def one(p):
            rc, log = run(a.tree, exes[p[0]], p[1])
            (a.receipts / f"{p[0]}.log").write_text(log)
            return summarize(p[0], p[1], rc, log)
        with cf.ThreadPoolExecutor(8) as pool:
            rows = list(pool.map(one, sel))
        out = a.receipts / "summary.tsv"
    out.write_text("\n".join(rows) + "\n")
    print("\n".join(rows))


if __name__ == "__main__":
    sys.exit(main())

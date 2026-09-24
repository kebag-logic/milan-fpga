#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R299-2 reviewer mutation check of the random sigma-context probe.

Each mutant is one or more exact textual edits of hdl/srp/KL_srp_admission.sv
in a private copy of the exact-head tree under <work>; run_sigma_probe.sh then
runs against it for each (N, mode) configuration. KILLED = the probe exits
non-zero with a 'checks:' tally; a build failure is BUILD-FAIL, never a kill.
Usage: mutants_r2.py <head-tree> <work> <out-dir> [jobs] [seeds]
"""
import concurrent.futures as cf
from pathlib import Path
import shutil
import subprocess
import sys

ADM = "hdl/srp/KL_srp_admission.sv"
PEND = "assign pend_w   = !invalid_w[aidx_r] && !slope_valid_r[aidx_r];"
MUTANTS = {
    "control": [],
    # round 1 design: a pending source counts as absent
    "A-pending-absent": [(PEND, "assign pend_w   = 1'b0;", 1)],
    # both stale protections removed
    "B-stale-both": [(" && slope_valid_r[aidx_r]", "", 2), (PEND, "assign pend_w   = 1'b0;", 1)],
    # a discarded round still strobes round_done_o
    "C-discard-strobes": [("          round_done_o <= 1'b1;\n        end\n",
                           "        end\n        round_done_o <= 1'b1;\n", 1)],
    # a pending LAST source (visited on the publishing clock) is not seen
    "D-last-visit-ignored": [("if (!(pend_acc_r || pend_w)) begin", "if (!pend_acc_r) begin", 1)],
    # pending is not accumulated across the round
    "E-pend-not-accumulated": [("pend_acc_r <= pend_acc_r | pend_w;", "pend_acc_r <= pend_w;", 1)],
    # round 1 validity terms only (author: equivalent under the discard)
    "F-validity-terms-only": [(" && slope_valid_r[aidx_r]", "", 2)],
    # declaration does not retire its own grant
    "G-no-immediate-retire": [("grant_r    <= grant_r & ~invalid_w;", "grant_r    <= grant_r;", 1)],
    # declaration does not restart the partial round
    "H-no-round-restart": [("      if (|invalidate_i) begin\n", "      if (1'b0) begin\n", 1)],
    # a discarded round publishes the aggregate anyway (grants still held)
    "I-aggregate-not-frozen": [("        if (!(pend_acc_r || pend_w)) begin\n          grant_r      <= wgrant_now_w;\n          gslope_r     <= wgslope_now_w;\n",
                                "        sum_r        <= fit_w ? cand_w[31:0] : acc_r;\n        if (!(pend_acc_r || pend_w)) begin\n          grant_r      <= wgrant_now_w;\n          gslope_r     <= wgslope_now_w;\n", 1)],
}
CONFIGS = [("3", "multi"), ("8", "single")]


def mutate(head, tree, edits):
    shutil.copytree(head / "hdl", tree / "hdl")
    shutil.copytree(head / "tb" / "srp_admission", tree / "tb" / "srp_admission",
                    ignore=shutil.ignore_patterns("obj_*"))
    for old, new, count in edits:
        p = tree / ADM
        s = p.read_text()
        if s.count(old) != count:
            raise RuntimeError(f"anchor count {s.count(old)} != {count}: {old!r}")
        p.write_text(s.replace(old, new))


def run(name, cfg):
    n, mode = cfg
    tree = WORK / f"{name}-{n}-{mode}"
    if tree.exists():
        shutil.rmtree(tree)
    mutate(HEAD, tree, MUTANTS[name])
    log = OUT / f"{name}-N{n}-{mode}.log"
    with log.open("w") as f:
        r = subprocess.run(["sh", str(HERE / "run_sigma_probe.sh"), str(tree), n,
                            str(tree / "obj"), mode, SEEDS],
                           stdout=f, stderr=subprocess.STDOUT, timeout=3600, check=False)
    text = log.read_text()
    tally = [l for l in text.splitlines() if "checks:" in l]
    rules = sorted({l.split(" N=")[0][6:] for l in text.splitlines() if l.startswith("FAIL: ")})
    if not tally:
        verdict = "BUILD-FAIL"
    elif name == "control":
        verdict = "PASS" if r.returncode == 0 else "CONTROL-FAIL"
    else:
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    shutil.rmtree(tree)
    return name, f"N{n}-{mode}", r.returncode, verdict, tally[-1] if tally else "", rules


if __name__ == "__main__":
    HERE = Path(__file__).resolve().parent
    HEAD = Path(sys.argv[1]).resolve()
    WORK, OUT = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    JOBS = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    SEEDS = sys.argv[5] if len(sys.argv) > 5 else "50"
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = [(m, c) for m in MUTANTS for c in CONFIGS]
    with cf.ThreadPoolExecutor(max_workers=JOBS) as ex:
        res = list(ex.map(lambda t: run(*t), tasks))
    for name, cfg, rc, verdict, tally, rules in sorted(res):
        print(f"{name:24s} {cfg:10s} rc={rc:<3d} {verdict:10s} {tally} | {'; '.join(rules)}")

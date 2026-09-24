#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R299-1 reviewer mutation campaign for PR #114 (issue #112).

Each mutant is a single textual edit of the exact-head source, applied in a
private copy of the tree under <work>; the author's suites (tb/srp_admission
N=2 and N=8, tb/srp_top) and the reviewer probes then run against it.
A mutant is KILLED by a bench when that bench exits non-zero with a
'checks:' tally printed (a build failure is reported as BUILD-FAIL, never
as a kill). Usage: mutants_r299.py <head-tree> <work> <out-dir> [jobs]
"""
import concurrent.futures as cf
import os
from pathlib import Path
import shutil
import subprocess
import sys

ADM = "hdl/srp/KL_srp_admission.sv"
TOP = "hdl/srp/KL_srp_top.sv"
MUTANTS = {
    "control": [],
    "M1-stale-evaluation": [(ADM, " && slope_valid_r[aidx_r]", "", 2)],
    "M2-no-stage1-invalidate": [(ADM, "valid_q1_r <= !invalid_w[cidx_r];", "valid_q1_r <= 1'b1;", 1)],
    "M3-no-stage2-invalidate": [(ADM, "valid_q2_r <= valid_q1_r && !invalid_w[cidx_q1_r];",
                                 "valid_q2_r <= valid_q1_r;", 1)],
    "M4-no-stage3-override": [(ADM, "if (invalid_w[s]) slope_valid_r[s] <= 1'b0;",
                               "if (!req_i[s]) slope_valid_r[s] <= 1'b0;", 1)],
    "M5-no-round-restart": [(ADM, "      if (|invalidate_i) begin\n", "      if (1'b0) begin\n", 1)],
    "M6-no-immediate-retire": [(ADM, "grant_r    <= grant_r & ~invalid_w;", "grant_r    <= grant_r;", 1)],
    "M7-top-no-strobe": [(TOP, "if (gate_acc_w) adm_invalidate_w", "if (1'b0) adm_invalidate_w", 1)],
}
BENCHES = {
    "adm2": ("tb/srp_admission", ["make", "run", "N=2"]),
    "adm8": ("tb/srp_admission", ["make", "run", "N=8"]),
    "srp_top": ("tb/srp_top", ["make", "run"]),
}


def mutate(head, tree, edits):
    shutil.copytree(head, tree, symlinks=True,
                    ignore=shutil.ignore_patterns("obj_*", "obj_dir"))
    for rel, old, new, count in edits:
        p = tree / rel
        s = p.read_text()
        if s.count(old) != count:
            raise RuntimeError(f"{rel}: anchor count {s.count(old)} != {count}: {old!r}")
        p.write_text(s.replace(old, new))


def run(name, bench, work, out):
    tree = work / f"{name}-{bench}"
    if tree.exists():
        shutil.rmtree(tree)
    mutate(HEAD, tree, MUTANTS[name])
    sub, cmd = BENCHES[bench]
    log = out / f"{name}-{bench}.log"
    with log.open("w") as f:
        r = subprocess.run(cmd, cwd=tree / sub, stdout=f, stderr=subprocess.STDOUT,
                           timeout=3600, check=False)
    text = log.read_text()
    tally = [l for l in text.splitlines() if "checks:" in l]
    if not tally:
        verdict = "BUILD-FAIL"
    elif name == "control":
        verdict = "PASS" if r.returncode == 0 and " 0 FAIL" in tally[-1] else "CONTROL-FAIL"
    else:
        verdict = "KILLED" if r.returncode != 0 else "SURVIVED"
    shutil.rmtree(tree)
    return name, bench, r.returncode, verdict, tally[-1] if tally else ""


if __name__ == "__main__":
    HEAD = Path(sys.argv[1]).resolve()
    work, out = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    tasks = [(m, b) for m in MUTANTS for b in BENCHES]
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        res = list(ex.map(lambda t: run(t[0], t[1], work, out), tasks))
    for name, bench, rc, verdict, tally in sorted(res):
        print(f"{name:26s} {bench:8s} rc={rc:<3d} {verdict:12s} {tally}")

#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned mutants (R298-1) against the #112 fix.

Each mutant edits one construct of the head RTL in a disposable copy and
runs the head's own suites against it. A mutant is KILLED when a suite
exits non-zero with a readable tally; a build failure is reported as
BUILD-ERROR, never as a kill.
Usage: mutants_r298.py <head-tree> <verilator> <work-dir> <out-dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, VL, WORK, OUT = (Path(a) for a in sys.argv[1:5])
ADM = "hdl/srp/KL_srp_admission.sv"
TOP = "hdl/srp/KL_srp_top.sv"

MUTANTS = [
    # name, file, old, new, suites
    ("A1-no-stage-invalidation", ADM,
     "      valid_q1_r <= !invalid_w[cidx_r];\n      valid_q2_r <= valid_q1_r && !invalid_w[cidx_q1_r];\n",
     "      valid_q1_r <= 1'b1;\n      valid_q2_r <= valid_q1_r;\n",
     ["adm1", "adm2", "adm8", "srp_top"]),
    ("A2-no-final-override", ADM,
     "        if (invalid_w[s]) slope_valid_r[s] <= 1'b0;\n",
     "        if (1'b0 && invalid_w[s]) slope_valid_r[s] <= 1'b0;\n",
     ["adm1", "adm2", "adm8", "srp_top"]),
    ("A3-no-grant-retire", ADM,
     "        grant_r    <= grant_r & ~invalid_w;\n",
     "        grant_r    <= grant_r;\n",
     ["adm2", "adm8", "srp_top"]),
    ("A4-no-round-restart", ADM,
     "        aidx_r     <= '0;\n        acc_r      <= 32'd0;\n        over_acc_r <= 1'b0;\n        wgrant_r   <= '0;\n        wgslope_r  <= '0;\n      end else if (round_w) begin",
     "      end else if (round_w) begin",
     ["adm2", "adm8", "srp_top"]),
    ("A5-fit-ignores-invalid", ADM,
     "  assign fit_w    = !invalid_w[aidx_r] && slope_valid_r[aidx_r]",
     "  assign fit_w    = slope_valid_r[aidx_r]",
     ["adm2", "adm8", "srp_top"]),
    ("A6-stage1-only", ADM,
     "      valid_q2_r <= valid_q1_r && !invalid_w[cidx_q1_r];\n",
     "      valid_q2_r <= valid_q1_r;\n",
     ["adm1", "adm2", "adm8", "srp_top"]),
    ("T1-top-no-invalidate-strobe", TOP,
     "    if (gate_acc_w) adm_invalidate_w[a_idx_r[SRC_W_C-1:0]] = 1'b1;\n",
     "    if (1'b0) adm_invalidate_w[a_idx_r[SRC_W_C-1:0]] = 1'b1;\n",
     ["srp_top"]),
]

SUITES = {
    "adm1": ("tb/srp_admission", ["run", "N=1"]),
    "adm2": ("tb/srp_admission", ["run", "N=2"]),
    "adm8": ("tb/srp_admission", ["run", "N=8"]),
    "srp_top": ("tb/srp_top", ["run"]),
}


def run(tree, suite, log):
    d, args = SUITES[suite]
    with log.open("w") as f:
        r = subprocess.run(["make", f"VERILATOR={VL}", *args], cwd=tree / d,
                           stdout=f, stderr=subprocess.STDOUT, timeout=3600)
    text = log.read_text()
    tally = [l for l in text.splitlines() if " checks: " in l and " PASS, " in l]
    return r.returncode, (tally[-1] if tally else "")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []
    survivors = 0
    for name, rel, old, new, suites in MUTANTS:
        tree = WORK / name
        shutil.rmtree(tree, ignore_errors=True)
        tree.mkdir(parents=True)
        for sub in ("hdl", "tb/common", "tb/srp_admission", "tb/srp_top"):
            shutil.copytree(HEAD / sub, tree / sub,
                            ignore=shutil.ignore_patterns("obj_*", "obj_dir"))
        src = (tree / rel).read_text()
        if src.count(old) != 1:
            lines.append(f"{name}: ANCHOR-MISSING")
            survivors += 1
            continue
        (tree / rel).write_text(src.replace(old, new))
        killed = False
        for s in suites:
            rc, tally = run(tree, s, OUT / f"{name}-{s}.log")
            verdict = ("KILLED" if rc != 0 and tally else
                       "BUILD-ERROR" if rc != 0 else "survived")
            killed |= verdict == "KILLED"
            lines.append(f"{name} {s}: rc={rc} {verdict} [{tally}]")
            print(lines[-1], flush=True)
        lines.append(f"{name}: {'KILLED' if killed else 'SURVIVED'}")
        print(lines[-1], flush=True)
        survivors += not killed
        shutil.rmtree(tree, ignore_errors=True)
    (OUT / "summary.txt").write_text("\n".join(lines) + "\n")
    print(f"{len(MUTANTS)} mutants, {len(MUTANTS) - survivors} killed, {survivors} survived")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

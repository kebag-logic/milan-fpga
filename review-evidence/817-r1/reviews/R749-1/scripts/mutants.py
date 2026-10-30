#!/usr/bin/env python3
"""Planted-mutant campaign for the #817 servo reset synchronizer cut and its gates.

Usage: mutants.py <clean-tree> <scratch-dir> <out-dir> <python-with-litex> [--jobs N]

Each mutant is one exact textual replacement (asserted to match exactly once)
in a private copy of the tree. Stub mutants run the Tcl stub test only; build
mutants run one shipping elaboration (no vendor tool). A mutant is KILLED when
its gate exits non-zero AND the log carries the expected refusal text. Two
unmutated controls must pass in copies made the same way.
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

TCL = "sw/litex/clock_constraints.tcl"
PY = "sw/litex/clock_constraints.py"
SOC = "sw/litex/milan_soc.py"

STUB = ("-c", "import sys; sys.path.insert(0, 'sw/builder'); "
              "import test_clock_constraints as t; t.test_servo_reset_sync()")
SHIP = ("-B", "sw/builder/test_shipping_clock_constraints.py",
        "--config", "ax7101_1x1_tdm8", "--port", "e1")

MUTANTS = [
    # name, kind, file, old, new, expected text in the failing log
    ("C0-control-stub", "stub", None, None, None, None),
    ("C1-control-ship", "ship", None, None, None, None),
    ("S1-cut-removed", "stub", TCL, "    set_false_path -from $src -to $pin\n", "",
     "servo cut missing or widened"),
    ("S2-cut-widened-no-from", "stub", TCL, "set_false_path -from $src -to $pin",
     "set_false_path -to $pin", "servo cut missing or widened"),
    ("S3-cut-on-second-stage", "stub", TCL, "set pin [get_pins -of_objects $first",
     "set pin [get_pins -of_objects $second", "servo cut missing or widened"),
    ("S4-cut-clock-level", "stub", TCL, "set_false_path -from $src -to $pin",
     "set_false_path -from $src -to $dst", "servo cut missing or widened"),
    ("S5-asyncreg-check-dropped", "stub", TCL,
     "if {![string is true -strict [get_property ASYNC_REG $cell]]} {", "if {0} {",
     "accepted: *lacks ASYNC_REG*"),
    ("S6-asyncreg-check-nonstrict", "stub", TCL,
     "string is true -strict [get_property ASYNC_REG $cell]",
     "string is true [get_property ASYNC_REG $cell]", "accepted: *lacks ASYNC_REG*"),
    ("S7-stage-count-check-dropped", "stub", TCL,
     "if {[llength $stages] != 2} {", "if {0} {", "wrong refusal"),
    ("S8-chain-check-dropped", "stub", TCL,
     "if {[llength $first] != 1 || [llength $second] != 1} {", "if {0} {",
     "not a two-flop chain"),
    ("S9-clock-check-dropped", "stub", TCL,
     "if {[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]} {", "if {0} {",
     "not one clock distinct from milan"),
    ("S10-clock-distinct-half-dropped", "stub", TCL,
     "if {[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]} {",
     "if {[llength $dst] != 1} {", "not one clock distinct from milan"),
    ("S11-clock-single-half-dropped", "stub", TCL,
     "if {[llength $dst] != 1 || [lindex $dst 0] eq [lindex $src 0]} {",
     "if {[lindex $dst 0] eq [lindex $src 0]} {", "not one clock distinct from milan"),
    ("S12-src-clock-unchecked", "stub", TCL,
     "    set src [kl_net_clock $milan_net]\n",
     "    set src [get_clocks -of_objects [get_nets $milan_net]]\n", "missing clock accepted"),
    ("E1-hook-call-removed", "ship", SOC,
     "                    add_servo_reset_constraints(platform, self.crg)\n",
     "                    pass\n", "hook missing, duplicated or renamed: []"),
    ("E2-hook-call-duplicated", "ship", SOC,
     "                    add_servo_reset_constraints(platform, self.crg)\n",
     "                    add_servo_reset_constraints(platform, self.crg)\n"
     "                    add_servo_reset_constraints(platform, self.crg)\n",
     "hook missing, duplicated or renamed"),
    ("E3-hook-names-sys-clock", "ship", SOC,
     "            self.milan_pll_clk = pll.clkouts[pll.nclkouts - 1].clk\n",
     "            self.milan_pll_clk = pll.clkouts[0].clk\n",
     "hook missing, duplicated or renamed"),
    ("E4-tcl-sourced-twice", "ship", PY,
     "    if source not in platform.toolchain.pre_optimize_commands:\n"
     "        platform.toolchain.pre_optimize_commands.append(source)\n",
     "    platform.toolchain.pre_optimize_commands.append(source)\n",
     "constraint Tcl sourced 2 times"),
    ("E5-hook-moved-pre-placement", "ship", PY,
     "    platform.toolchain.pre_optimize_commands.add(\n"
     "        \"kl_servo_reset_sync_constraints {milan}\"",
     "    platform.toolchain.pre_placement_commands.add(\n"
     "        \"kl_servo_reset_sync_constraints {milan}\"",
     "servo reset synchronizer hook outside pre-optimize"),
    ("E6-hook-skipped-with-servo-present", "ship", SOC,
     "if (optional_blocks or {}).get(\"media_clock_servo\", True):",
     "if (optional_blocks or {}).get(\"media_clock_servo\", False):",
     "hook missing, duplicated or renamed: []"),
]


def run(mutant, clean, scratch, out, python):
    name, kind, rel, old, new, expect = mutant
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(clean, tree, symlinks=True, ignore=shutil.ignore_patterns(".git"))
    if rel:
        path = tree / rel
        text = path.read_text()
        count = text.count(old)
        if count != 1:
            return dict(mutant=name, verdict="NOT-APPLIED", matches=count)
        path.write_text(text.replace(old, new))
    argv = [python, *(STUB if kind == "stub" else
                      (SHIP[0], str(tree / SHIP[1]), *SHIP[2:]))]
    if kind == "ship":
        argv += ["--output-dir", str(tree / "_elab")]
    cwd = tree if kind == "stub" else tree / "sw/litex"
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    start = time.time()
    proc = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=1200)
    log = proc.stdout + proc.stderr
    (out / f"{name}.log").write_text(log)
    if rel is None:
        verdict = "PASS" if proc.returncode == 0 and "PASS" in log else "CONTROL-FAILED"
    else:
        verdict = "KILLED" if proc.returncode != 0 and expect in log else (
            "SURVIVED" if proc.returncode == 0 else "FAILED-UNEXPECTEDLY")
    shutil.rmtree(tree, ignore_errors=True)
    return dict(mutant=name, kind=kind, file=rel, rc=proc.returncode,
                seconds=round(time.time() - start), expected=expect, verdict=verdict)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clean", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("python")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(lambda m: run(m, a.clean, a.scratch, a.out, a.python), MUTANTS))
    (a.out / "mutants.json").write_text(json.dumps(results, indent=1) + "\n")
    for r in results:
        print(f"{r['mutant']:40s} {r['verdict']} rc={r.get('rc')} {r.get('seconds', '')}s")
    ok = all(r["verdict"] == ("PASS" if r["mutant"].startswith("C") else "KILLED") for r in results)
    print("CAMPAIGN", "ALL-KILLED-CONTROLS-PASS" if ok else "NOT-CLEAN")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

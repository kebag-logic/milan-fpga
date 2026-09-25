#!/usr/bin/env python3
"""Run ONE control of a repository mutation campaign through the campaign's
own functions, so a long campaign can be split into bounded invocations.

usage:
  run_one_control.py <repo> gmstep  anchors
  run_one_control.py <repo> gmstep  positive <leg>     (gmstep | option-off)
  run_one_control.py <repo> gmstep  control  <index>   (index into CONTROLS)
  run_one_control.py <repo> crflic  anchors
  run_one_control.py <repo> crflic  positive
  run_one_control.py <repo> crflic  mutant   <index>   (index into MUTATIONS)

The planted copy and its build directory live under $WORK (default: a fresh
temporary directory), never inside the checkout. The verdict logic, anchors,
recipes and named checks are the campaign module's own; this file only
selects which entry runs. Exit 0 when the entry passed (the positive control
passes, the control is caught), 1 otherwise.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path


def load(repo: Path, name: str):
    path = repo / "tb/verilator/milan_dp" / f"{name}_mutants.py"
    spec = importlib.util.spec_from_file_location(f"{name}_mutants", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    campaign, action = sys.argv[2], sys.argv[3]
    arg = sys.argv[4] if len(sys.argv) > 4 else None
    mod = load(repo, campaign)
    work = Path(os.environ.get("WORK") or tempfile.mkdtemp(prefix=f"{campaign}-one-"))
    work.mkdir(parents=True, exist_ok=True)
    if campaign == "gmstep":
        if action == "anchors":
            bad = 0
            for i, c in enumerate(mod.CONTROLS):
                n = mod.SOURCES[c.source].resolve().read_text().count(c.anchor)
                print(f"gmstep control {i:2d} anchor count {n} leg {c.leg:10s} {c.name}")
                bad += n != 1
            print(f"gmstep anchors: {len(mod.CONTROLS)} controls, {bad} not exactly once")
            return 1 if bad else 0
        if action == "positive":
            leg = mod.LEGS[arg]
            exe = mod.build(leg, {}, work / f"obj_clean_{leg.target}")
            answer = mod.verdict(*mod.run_leg(leg, exe), None) if exe else "did not compile"
            print(f"positive {arg}: {answer}")
            return 0 if answer == "pass" else 1
        control = mod.CONTROLS[int(arg)]
        print(f"control {arg}: {control.name} (leg {control.leg}, must break "
              f"{control.breaks!r})")
        return 0 if mod.run_control(control, work, int(arg)) else 1
    if campaign == "crflic":
        src = mod.DP_RTL.resolve().read_text()
        if action == "anchors":
            bad = 0
            for i, m in enumerate(mod.MUTATIONS):
                n = src.count(m[1])
                print(f"crflic mutant {i} anchor count {n}: {m[0]}")
                bad += n != 1
            print(f"crflic anchors: {len(mod.MUTATIONS)} mutants, {bad} not exactly once")
            return 1 if bad else 0
        if action == "positive":
            exe = mod.build(mod.DP_RTL.resolve(), work / "obj_clean")
            answer = mod.verdict(*mod.run_leg(exe), None) if exe else "did not compile"
            print(f"positive crflic: {answer}")
            return 0 if answer == "pass" else 1
        return 0 if mod.run_mutant(src, mod.MUTATIONS[int(arg)], work) else 1
    print(f"unknown campaign {campaign}")
    return 2


if __name__ == "__main__":
    sys.exit(main())

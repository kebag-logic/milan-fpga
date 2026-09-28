#!/usr/bin/env python3
"""R369-3 reviewer probe (S7): can the new portable dispatch controls fail?

Usage: dispatch_control_mutants.py REPO_ROOT
Loads tb/verilator/fw_service_budget/run.py from its own path, with one
planted change at a time (text substitution in memory; the file is not
edited), and runs the committed dispatch_controls() and service_controls().
Each planted oracle defect must raise; the unmodified source must pass.
"""
import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PATH = ROOT / "tb/verilator/fw_service_budget/run.py"
SRC = PATH.read_text()
sys.path.insert(0, str(PATH.parent))

MUTANTS = {
    "none": None,
    "per-line oracle removed": (
        "                findings.append('console line lacks a dispatch opportunity: ' + row['duty'])",
        "                pass"),
    "per-line oracle limited to queued-builtins (round-2 scope)": (
        "result['media']['plan'] in ('queued-builtins', 'queued-short')",
        "result['media']['plan'] == 'queued-builtins'"),
    "verdict per-line requirement removed (round-2 verdict)": (
        "        require(any(item.startswith('console line lacks a dispatch opportunity: ') for item in findings),\n"
        "                'dispatch removal escaped per-line check')\n", ""),
    "per-line oracle fires on every row (over-eager)": (
        "            if row['tick_calls'] == 0:", "            if True:"),
}


def load(src):
    mod = types.ModuleType("run_mut")
    mod.__file__ = str(PATH)
    exec(compile(src, str(PATH), "exec"), mod.__dict__)
    return mod


fails = []
for name, sub in MUTANTS.items():
    src = SRC
    if sub:
        if SRC.count(sub[0]) != 1:
            print(f"{name}: ANCHOR NOT UNIQUE ({SRC.count(sub[0])})")
            fails.append(name)
            continue
        src = SRC.replace(sub[0], sub[1])
    mod = load(src)
    results = []
    for fn in ("dispatch_controls", "service_controls"):
        try:
            n = getattr(mod, fn)()
            results.append(f"{fn}=pass({n})")
        except RuntimeError as e:
            results.append(f"{fn}=RAISED({e})")
    raised = any("RAISED" in r for r in results)
    ok = (not raised) if sub is None else raised
    print(f"{name:<58} {'KILLED' if raised and sub else ('PASS' if not raised else 'FAILED')} :: {'; '.join(results)}")
    if not ok:
        fails.append(name)
print("RESULT:", "FAIL " + str(fails) if fails else "PASS")
sys.exit(1 if fails else 0)

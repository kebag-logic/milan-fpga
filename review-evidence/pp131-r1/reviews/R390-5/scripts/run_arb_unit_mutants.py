#!/usr/bin/env python3
"""R390-5: run the reviewer's arbiter unit probe (carried from R390-4) at the head
and against each r5_extra_mutants.py arbiter edit, each in its own scratch copy.
Usage: run_arb_unit_mutants.py <tree> <scratch-dir> <verilator>"""
import importlib.util, shutil, subprocess, sys
from pathlib import Path
tree, scratch, vl = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("d3", tree / "tb/pp_top/d3_mutants.py")
d3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(d3)
spec = importlib.util.spec_from_file_location("r5x", here / "r5_extra_mutants.py")
r5x = importlib.util.module_from_spec(spec); spec.loader.exec_module(r5x)
runs = {"head": ()}
runs.update(r5x.edits(d3))
for name in ("issue_arm_cross_intent",):
    runs[name] = next(m.edits for m in d3.MUTANTS if m.name == name)
for name, edits in runs.items():
    copy = scratch / name
    shutil.rmtree(copy, ignore_errors=True)
    (copy / "hdl/packet_engine").mkdir(parents=True)
    shutil.copy(tree / "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv", copy / "hdl/packet_engine/")
    assert d3.plant(copy, edits) == ""
    out = subprocess.run(["sh", str(here / "arb_unit/run_arb_unit.sh"), str(copy),
                          str(copy / "build"), vl], capture_output=True, text=True).stdout
    tally = [l for l in out.splitlines() if "checks" in l.lower() or l.startswith("rc=")]
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    print(f"== {name}: {' | '.join(tally)}")
    for f in fails: print("   " + f[:180])

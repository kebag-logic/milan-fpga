#!/usr/bin/env python3
"""List every failing check of each crf_rx engine-and-replica #762 mutant.

Usage: crf_both_mutant_failures.py <tree-root> <work-dir>
Uses tb/verilator/crf_rx/mutants.py's own BOTH_MUTANTS table and plant(); the
tree is a disposable copy of the reviewed head and is not edited.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
here = root / "tb/verilator/crf_rx"
spec = importlib.util.spec_from_file_location("crf_mutants", here / "mutants.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rtl = (root / "hdl/ieee1722/crf/KL_crf_rx.sv").read_text()
cpp = (here / "sim_main.cpp").read_text()
status = 0
for name, rtl_edits, replica_edits, failure in mod.BOTH_MUTANTS:
    r = mod.plant(rtl, rtl_edits)
    c = mod.plant(cpp, replica_edits)
    if r is None or c is None:
        print(f"{name}: anchor not unique")
        status = 1
        continue
    (work / f"{name}.sv").write_text(r)
    (work / f"{name}.cpp").write_text(c)
    mdir = work / f"obj_{name}"
    subprocess.run(["make", "-s", "-C", str(here), "unit-build", f"RX_RTL={work / (name + '.sv')}",
                    f"UNIT_MDIR={mdir}", f"UNIT_CPP={work / (name + '.cpp')}"],
                   check=True, capture_output=True)
    run = subprocess.run([str(mdir / "Vcrf_rx_sim")], capture_output=True, text=True, cwd=here)
    fails = [ln for ln in run.stdout.splitlines() if "FAIL" in ln or "MISMATCH" in ln.upper()]
    print(f"== {name}: rc={run.returncode}, named check {failure!r}, failing lines {len(fails)}")
    for ln in fails:
        print("   " + ln)
    print("   " + run.stdout.strip().splitlines()[-1])
sys.exit(status)

#!/usr/bin/env python3
"""Break gate 1h's own reader five ways in a disposable clone; each must turn the gate red.

Usage: gate_mutants.py <disposable clone>; the front end is whatever is first on PATH.
"""
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1])
src = (clone / "sw/builder/test_builder.py").read_text()
GATE = "test_gptp_datapath_carries_the_launch_shape"
MUTANTS = {
    "m1_reads_raw_text": ('return read.stdout, ""', 'return rtl, ""'),
    "m2_no_defines": ('*(f"-D{define}" for define in record["define"]),\n', ""),
    "m3_no_plane_count": ("if len(planes) != 1:", "if False:"),
    "m4_default_any_value": ('if declared != [("parameter", str(default))]:', "if not declared:"),
    "m5_binding_any_member": ("if bound != [param]:", "if param not in bound:"),
}
procs = {}
for name, (old, new) in MUTANTS.items():
    assert src.count(old) == 1, old
    path = clone / "sw/builder" / f"{name}.py"
    path.write_text(src.replace(old, new))
    procs[name] = (path, subprocess.Popen([sys.executable, str(path), "--gates", GATE], cwd=clone,
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True))
wrong = 0
for name, (path, proc) in procs.items():
    out = proc.communicate()[0]
    path.unlink()
    last = out.strip().splitlines()[-1][:190]
    wrong += proc.returncode == 0
    print(f"{name}: rc {proc.returncode}: {last}")
print("mutants:", len(MUTANTS), "left green:", wrong)
sys.exit(1 if wrong else 0)

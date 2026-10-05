#!/usr/bin/env python3
"""Exercise the production ADP checker and kill an overly wide exemption."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

root, scratch = (Path(arg).resolve() for arg in sys.argv[1:])
sys.path.insert(0, str(root / "tb/tools"))
from avtp_wire_truth_checks import WireTruth
from avtp_wire_truth_frames import build_adp_frame

cases = {
    "whole_cycle": ([(0, 3), (0, 4), (1, 5), (0, 0), (0, 1)], "PASS"),
    "depart_before_first_available": ([(1, 0), (0, 0), (0, 1)], "PASS"),
    "repeat_after_reset": ([(1, 5), (0, 0), (0, 0)], "FAIL"),
    "departing_nonzero_repeat": ([(0, 4), (1, 5), (0, 5)], "FAIL"),
    "ordinary_repeat": ([(0, 4), (0, 4)], "FAIL"),
    "ordinary_wrap": ([(0, 0xffffffff), (0, 0)], "PASS"),
}
for name, (seq, expected) in cases.items():
    reader = WireTruth()
    for i, (kind, index) in enumerate(seq):
        reader.feed(float(i), build_adp_frame(message_type=kind, available_index=index))
    results = [v for v in reader.check_adp_frame_rule() if "available-index" in v.check]
    assert len(results) == 1
    result = results[0]
    print(json.dumps({"case": name, "expected": expected, "actual": result.verdict,
                      "detail": result.detail}, sort_keys=True), flush=True)
    assert result.verdict == expected

copy = scratch / "wide-exemption"
copy.mkdir(parents=True, exist_ok=True)
for path in (root / "tb/tools").glob("avtp_wire_truth*.py"):
    shutil.copy2(path, copy / path.name)
path = copy / "avtp_wire_truth_checks.py"
source = path.read_text()
old = "and idx[i][1] == 0}"
assert source.count(old) == 1
path.write_text(source.replace(old, "and True}"))
run = subprocess.run([sys.executable, "avtp_wire_truth.py", "--self-test"], cwd=copy,
                     capture_output=True, text=True, timeout=60)
print("WIDER EXEMPTION MUTANT OUTPUT", flush=True)
print(run.stdout + run.stderr)
assert run.returncode != 0
assert "FAIL: test_available_index_resets_after_departing" in run.stderr
assert "AssertionError: 'PASS' != 'FAIL'" in run.stderr
print("WIDER EXEMPTION KILLED by new committed test; rc=" + str(run.returncode))

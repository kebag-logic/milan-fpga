#!/usr/bin/env python3
"""Directed wire inputs and three disposable exemption defects."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "tb/tools"))
from avtp_wire_truth_checks import WireTruth
from avtp_wire_truth_frames import build_adp_frame

cases = [
    ("consecutive-advertisements", [(0, 0), (0, 1)], "PASS"),
    ("depart-before-first-advertisement", [(1, 0), (0, 0), (0, 1)], "PASS"),
    ("complete-cycle", [(0, 3), (0, 4), (1, 5), (0, 0), (0, 1)], "PASS"),
    ("repeated-advertisement", [(0, 4), (0, 4)], "FAIL"),
    ("repeat-after-reset", [(1, 5), (0, 0), (0, 0)], "FAIL"),
    ("retained-departing-index", [(0, 4), (1, 5), (0, 5)], "FAIL"),
    ("counter-wrap", [(0, 0xffffffff), (0, 0)], "PASS"),
]
for name, sequence, expected in cases:
    wt = WireTruth()
    for message_type, index in sequence:
        wt.feed(0.0, build_adp_frame(message_type=message_type, available_index=index))
    verdict = [v for v in wt.check_adp_frame_rule() if "available-index" in v.check][0]
    print(json.dumps({"case": name, "sequence": sequence, "expected": expected,
                      "observed": verdict.verdict, "detail": verdict.detail}), flush=True)
    assert verdict.verdict == expected, name

source = root / "tb/tools"
original = (source / "avtp_wire_truth_checks.py").read_text()
mutations = [
    ("reset-exemption-removed", "and i not in resets]", "]"),
    ("nonzero-reset-exempt", "and idx[i][1] == 0}", "and True}"),
    ("any-zero-exempt", "if idx[i - 1][0] == ADP_ENTITY_DEPARTING", "if True"),
]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0",
           TMPDIR=str(packet / "scratch/tmp"))
for name, old, new in mutations:
    assert original.count(old) == 1, name
    dest = packet / "scratch" / name
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns("__pycache__"), dirs_exist_ok=True)
    (dest / "avtp_wire_truth_checks.py").write_text(original.replace(old, new))
    result = subprocess.run([sys.executable, str(dest / "avtp_wire_truth.py"), "--self-test"],
                            cwd=root, env=env, capture_output=True, timeout=60)
    output = result.stdout + result.stderr
    (packet / "receipts" / (name + ".log")).write_bytes(output)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    assert result.returncode == 1 and b"test_available_index_resets_after_departing" in output
    print(json.dumps({"mutation": name, "rc": result.returncode,
                      "detected_by": "test_available_index_resets_after_departing"}), flush=True)
print("PASS: seven directed inputs; three planted defects detected")

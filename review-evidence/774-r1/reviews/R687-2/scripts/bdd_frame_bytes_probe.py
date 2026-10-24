#!/usr/bin/env python3
"""Apply tests/steps/crf_class_a_steps.py's own _localparam_int resolver to
KL_crf_tx.sv at two commits, the check behind the BDD scenario
"The tag replaces pad, it does not resize the frame" (FRAME_BYTES == 60).

usage: python3 bdd_frame_bytes_probe.py <repo> <commit> [<commit> ...]
Prints one line per commit; exit 1 if any commit does not resolve to 60.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "crf_class_a_steps", repo / "tests/steps/crf_class_a_steps.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
bad = 0
for commit in sys.argv[2:]:
    src = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:hdl/ieee1722/crf/KL_crf_tx.sv"],
                         check=True, capture_output=True, text=True).stdout
    for name in ("CRF_PDU_C", "FRAME_BYTES"):
        try:
            val = mod._localparam_int(src, name)
            print(f"{commit} {name} = {val}")
            if name == "FRAME_BYTES" and val != 60:
                bad += 1
        except AssertionError as exc:
            print(f"{commit} {name}: ASSERT FAILED: {exc}")
            bad += 1
sys.exit(1 if bad else 0)

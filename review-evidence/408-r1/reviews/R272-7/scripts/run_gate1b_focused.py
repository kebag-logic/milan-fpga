#!/usr/bin/env python3
"""Run ONLY gate 1b (test_baremetal_profile_contract) of a candidate tree.

Usage: run_gate1b_focused.py <candidate-clone> [--require-rv32]

Imports sw/builder/test_builder.py from the candidate (its __main__ guard
keeps the rest of the builder bank from running) and calls the one gate
function. The compiler and verilator are whatever the caller's PATH and
HOME provide; the gate itself records which compiler answered.
"""
import importlib.util
import sys
import time
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.argv = [str(clone / "sw/builder/test_builder.py")] + sys.argv[2:]
sys.path.insert(0, str(clone / "sw/builder"))
spec = importlib.util.spec_from_file_location(
    "test_builder", clone / "sw/builder/test_builder.py")
module = importlib.util.module_from_spec(spec)
sys.modules["test_builder"] = module
spec.loader.exec_module(module)
start = time.monotonic()
module.test_baremetal_profile_contract()
print(f"FOCUSED gate 1b PASS in {time.monotonic() - start:.0f}s "
      f"argv={sys.argv[1:]}", flush=True)

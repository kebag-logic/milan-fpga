#!/usr/bin/env python3
"""Reviewer run of the four builder gates this PR adds or changes, and nothing else of test_builder.py:
gate 23d (the prune guard, its accepted and refused spellings), gate 23m (the SoC binds what the
builder states, now with a split case) and its mutation arm, and gate 23n (control.placement).

Usage: builder_gates.py <repo checkout>   (run with the LiteX environment on PYTHONPATH)
"""
import sys
import time
import traceback
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/builder"))
import test_builder as tb  # noqa: E402

GATES = ("test_optional_block_names_reach_the_rtl", "test_control_placement_key",
         "test_datapath_params_match_the_instance", "test_datapath_params_gate_bites")
bad = 0
for name in GATES:
    t0 = time.time()
    try:
        getattr(tb, name)()
        print(f"PASS {name} ({time.time() - t0:.0f} s)", flush=True)
    except Exception:  # noqa: BLE001 - report and continue
        bad += 1
        print(f"FAIL {name} ({time.time() - t0:.0f} s)\n{traceback.format_exc()[-3000:]}", flush=True)
print(f"builder gates: {len(GATES) - bad} of {len(GATES)} pass")
sys.exit(1 if bad else 0)

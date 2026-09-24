#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R304-3: run the shipped engine mutation arm's own main() unchanged on a
slice of its own MUTATIONS list, so every slice fits one foreground window.
Each slice repeats the positive control. Exit status is main()'s.

usage: run_shipped_arm_slice.py EXPORTED_TREE START END
"""
import importlib.util
import sys
from pathlib import Path

tree, a, b = Path(sys.argv[1]).resolve(), int(sys.argv[2]), int(sys.argv[3])
eng = tree / "tb/verilator/engine"
sys.path.insert(0, str(eng))
spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
total = len(m.MUTATIONS)
m.MUTATIONS = m.MUTATIONS[a:b]
print(f"slice [{a}:{b}] of {total} shipped mutants", flush=True)
rc = m.main()
print(f"slice [{a}:{b}] rc={rc}", flush=True)
sys.exit(rc)

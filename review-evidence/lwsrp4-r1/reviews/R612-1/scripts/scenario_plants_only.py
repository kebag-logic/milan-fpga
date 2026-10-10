# SPDX-License-Identifier: Apache-2.0
"""Run only the scenario plants of a tree's tests/check_reversals.py. Usage: TREE WORK PREFIX"""
import importlib.util, sys
tree, work, prefix = sys.argv[1:4]
spec = importlib.util.spec_from_file_location("rev", f"{tree}/tests/check_reversals.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.CASES[:] = [c for c in mod.CASES if c[4] == "scenario"]
sys.argv = ["check_reversals.py", "--work-dir", work, "--prefix", prefix]
raise SystemExit(mod.main())

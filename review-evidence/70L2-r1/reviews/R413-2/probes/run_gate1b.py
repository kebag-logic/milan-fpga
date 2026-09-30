#!/usr/bin/env python3
"""Run ONLY test_baremetal_profile_contract (builder gate 1b and its
source rules) from a tree given as argv[1], with --require-rv32.
Usage: run_gate1b.py <tree>   (the tree's firmware may carry a plant)."""
import sys, time, importlib.util
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.argv = [str(tree / "sw/builder/test_builder.py"), "--require-rv32"]
sys.path.insert(0, str(tree / "sw/builder"))
spec = importlib.util.spec_from_file_location("test_builder", sys.argv[0])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
t = time.time()
try:
    mod.test_baremetal_profile_contract()
except AssertionError as exc:
    print("GATE REFUSED:", str(exc)[:1500])
    print(f"elapsed {time.time()-t:.1f}s")
    sys.exit(1)
print("GATE ACCEPTED (test_baremetal_profile_contract returned)")
print(f"elapsed {time.time()-t:.1f}s")

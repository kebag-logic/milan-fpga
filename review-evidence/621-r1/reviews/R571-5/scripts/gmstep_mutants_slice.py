#!/usr/bin/env python3
"""Run one round-robin slice of gmstep_mutants.py's whole inventory (--all).

usage: gmstep_mutants_slice.py <path to gmstep_mutants.py> <index> <count>
Slices partition CONTROLS by position; together they plant every control
exactly once on the whole leg. Each slice also runs the positive controls of
the legs its controls use. Nothing in the driver is changed.
"""
import importlib.util
import sys

path, index, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location("gmstep_mutants", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
full = list(module.CONTROLS)
module.CONTROLS = [c for i, c in enumerate(full) if i % count == index]
print(f"slice {index}/{count}: {len(module.CONTROLS)} of {len(full)} controls:", flush=True)
for c in module.CONTROLS:
    print(f"  - {c.name}", flush=True)
sys.argv = [path, "--all"]
sys.exit(module.main())

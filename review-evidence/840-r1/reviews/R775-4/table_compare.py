#!/usr/bin/env python3
"""Compare the shipped mutant table at the base and head of the round: argv[1] head tree, argv[2] base copy of test_phy_firmware.py."""
import importlib.util, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_phy_firmware as head
spec = importlib.util.spec_from_file_location("base_table", sys.argv[2])
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
a, b = base.ADVERTISEMENT_MUTANTS, head.ADVERTISEMENT_MUTANTS
print("base", len(a), "head", len(b))
print("added", sorted(set(b) - set(a)))
print("removed", sorted(set(a) - set(b)))
print("changed", sorted(k for k in a if k in b and a[k] != b[k]))

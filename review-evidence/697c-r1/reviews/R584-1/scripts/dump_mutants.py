#!/usr/bin/env python3
"""Dump ctrl_mutants.MUTANTS of the tree given (argv[1]) as JSON (argv[2]): name, path, old, new, kills."""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_mutants
out = [{"name": m.name, "path": m.path, "old": m.old, "new": m.new,
        "kills": [list(k) for k in m.kills()]} for m in ctrl_mutants.MUTANTS]
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(len(out), "mutants")

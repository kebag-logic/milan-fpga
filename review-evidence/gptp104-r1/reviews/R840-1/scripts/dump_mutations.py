#!/usr/bin/env python3
"""Dump an engine arm's MUTATIONS, one canonical JSON line per mutant.

usage: dump_mutations.py <tree-root> <out>
Imports <tree-root>/tb/verilator/engine/mutants.py by file path and writes
each (name, file, pattern, replacement, breaks) tuple as JSON, in order.
"""
import importlib.util
import json
import sys
from pathlib import Path

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location(
    "arm", root / "tb/verilator/engine/mutants.py")
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)
gen = sum(1 for m in arm.MUTATIONS if m[1] == arm.GENERATOR)
with out.open("w", encoding="utf-8") as f:
    for m in arm.MUTATIONS:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")
print(f"{len(arm.MUTATIONS)} mutants, {gen} generator-only, "
      f"{len(arm.MUTATIONS) - gen} RTL (built), names unique: "
      f"{len({m[0] for m in arm.MUTATIONS}) == len(arm.MUTATIONS)}")

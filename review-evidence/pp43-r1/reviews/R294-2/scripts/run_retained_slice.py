#!/usr/bin/env python3
"""Run the PR's retained tb/pp_top/gsi_mutants.py UNCHANGED on a slice of its
own mutation list (golden and restored controls included in every slice), so
each foreground call stays short. The module is imported from <tree>; only
its mutations() list is sliced, and only this reviewer's --output directory
is passed. TMPDIR should point inside the reviewer scratch directory.
Usage: run_retained_slice.py <tree> <start> <stop> <output> <verilator>
"""
import importlib.util
import sys
from pathlib import Path

tree, start, stop, output, verilator = sys.argv[1:6]
path = Path(tree) / "tb/pp_top/gsi_mutants.py"
spec = importlib.util.spec_from_file_location("gsi_mutants", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
full = mod.mutations()
print(f"retained list: {len(full)} mutations; slice [{start}:{stop}]", flush=True)
mod.mutations = lambda: full[int(start):int(stop)]
sys.argv = [str(path), "--output", output, "--verilator", verilator]
raise SystemExit(mod.main())

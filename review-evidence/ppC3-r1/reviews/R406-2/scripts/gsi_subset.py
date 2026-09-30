#!/usr/bin/env python3
"""Run tb/pp_top/gsi_mutants.py's own variants in a slice, reusing its check_variant()
and mutations() unchanged (the driver has no --only and runs past one call's limit).
usage: gsi_subset.py <tree> <output> <start> <stop> [--golden] [--restored]"""
import importlib.util, shutil, sys, tempfile
from pathlib import Path
tree_root, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
start, stop = int(sys.argv[3]), int(sys.argv[4])
spec = importlib.util.spec_from_file_location("gsi", tree_root / "tb/pp_top/gsi_mutants.py")
gsi = importlib.util.module_from_spec(spec); spec.loader.exec_module(gsi)
output.mkdir(parents=True, exist_ok=True)
variants = gsi.mutations()
print(f"variants total {len(variants)}; this slice {start}:{stop}", flush=True)
with tempfile.TemporaryDirectory(prefix="pp-gsi-subset-") as temp:
    tree = Path(temp)
    for d in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(tree_root / d, tree / d, ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    if "--golden" in sys.argv:
        gsi.check_variant(tree, output, "golden", "", "verilator")
    for name, filename, old, new, count, expected in variants[start:stop]:
        path = tree / filename; original = path.read_text()
        if original.count(old) != count:
            raise RuntimeError(f"{name}: expected {count} exact edit sites")
        try:
            path.write_text(original.replace(old, new))
            gsi.check_variant(tree, output, name, expected, "verilator")
        finally:
            path.write_text(original)
    if "--restored" in sys.argv:
        gsi.check_variant(tree, output, "restored", "", "verilator")
print("slice done", flush=True)

#!/usr/bin/env python3
"""Count flip-flop cells named armq_r in each run's baseline_cells.tsv (cell<TAB>primitive).

Usage: armq_count.py <label>=<baseline_cells.tsv> ...
"""
import hashlib, sys
for arg in sys.argv[1:]:
    label, path = arg.split("=", 1)
    data = open(path, "rb").read()
    rows = [line.split("\t") for line in data.decode().splitlines()[1:]]
    flops = sum(1 for cell, prim in rows if "armq_r" in cell.split("/")[-1] and prim.startswith("FD"))
    print(f"{label}: armq_r FD* cells {flops}; census sha256 {hashlib.sha256(data).hexdigest()}")

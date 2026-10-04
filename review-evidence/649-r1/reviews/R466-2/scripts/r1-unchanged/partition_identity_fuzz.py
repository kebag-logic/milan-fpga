#!/usr/bin/env python3
"""R466 probe: on random report hierarchies, the partition tie of resmap_map.py can
fail only when the ancestry tie has already failed (it is an identity of the
adjustments the ancestry step defines). Usage: partition_identity_fuzz.py <repo>"""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "syn/resmap"))
import resmap_map as M
rng = random.Random(649)
independent = 0
for trial in range(20000):
    keys = ["top"]
    for _ in range(rng.randint(1, 12)):
        parent = rng.choice([k for k in keys if not k.endswith("/@own")])
        keys.append(f"{parent}/n{len(keys)}")
    for k in list(keys):
        if any(o.startswith(k + "/") for o in keys) and rng.random() < 0.7:
            keys.append(f"{k}/@own")
    rows = {k: {c: rng.randint(0, 9) for c in M.COLUMNS} for k in keys}
    root, children = M.tree_of(rows)
    leaves = M.leaves_of(rows, children)
    anc, adj = M.ancestry_ties(rows, children)
    part = M.partition_ties(rows, root, leaves, adj)
    if part and not anc:
        independent += 1
print(f"trials 20000; partition failures with ancestry clean: {independent}")
sys.exit(1 if independent else 0)

#!/usr/bin/env python3
"""One shape of placement_identity.py's --dump, so a long dump splits across processes.

Usage: python3 identity_one_shape.py <head-repo> <tree> <shape-index> <out.json>
Runs <head-repo>/sw/mailbox/placement_identity.py's own dump() on <tree> with
only=<shape-index> (the function the tool's --dump and --selftest call), and
writes that shape's row. The tree's own census_elab.py elaborates it.
"""
import json
import sys
from pathlib import Path

head, tree, idx, out = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(head / "sw/mailbox"))
import placement_identity as pi  # noqa: E402

res = pi.dump(tree.resolve(), 1, None, only=idx)
out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
for s, v in res["shapes"].items():
    print(f"shape {s}: {v['digest']} ({v['cells']} cells, {v['nets']} nets)")

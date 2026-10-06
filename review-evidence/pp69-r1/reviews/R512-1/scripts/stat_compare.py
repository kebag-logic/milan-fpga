#!/usr/bin/env python3
"""Compare two Yosys `stat -json` files (base, head) for one top.

Usage: stat_compare.py BASE.json HEAD.json

Derived module names ($paramod$<hash>\\Name) are reduced to their base name so
the two sides pair up. Prints every differing field per module and a verdict
line: whether every cell count (num_cells and num_cells_by_type) is identical.
"""
import json
import re
import sys


def norm(name: str) -> str:
    return re.sub(r"^\$paramod\$[0-9a-f]+\\", lambda _m: "$paramod\\", name)


def load(path: str) -> dict:
    data = json.load(open(path))
    mods = {}
    for k, v in data["modules"].items():
        v = dict(v)
        if isinstance(v.get("num_cells_by_type"), dict):
            v["num_cells_by_type"] = {norm(t): n for t, n in v["num_cells_by_type"].items()}
        mods[norm(k)] = v
    return mods


def main() -> int:
    a, b = load(sys.argv[1]), load(sys.argv[2])
    cells_same = True
    diffs = 0
    for mod in sorted(set(a) | set(b)):
        if mod not in a or mod not in b:
            print(f"module only in {'head' if mod in b else 'base'}: {mod}")
            cells_same = False
            continue
        for key in sorted(set(a[mod]) | set(b[mod])):
            va, vb = a[mod].get(key), b[mod].get(key)
            if va != vb:
                diffs += 1
                print(f"{mod}: {key}: {va} -> {vb}")
                if key.startswith("num_cells") or key == "cells":
                    cells_same = False
    print(f"modules {len(a)} / {len(b)}; differing fields {diffs}; "
          f"every cell count identical: {cells_same}")
    return 0 if cells_same else 1


if __name__ == "__main__":
    raise SystemExit(main())

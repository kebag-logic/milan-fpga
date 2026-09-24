#!/usr/bin/env python3
"""Compare dumped gate 1b rows base vs head per mode (R317-1).
Usage: compare_rows.py DIR. Every base row (label + field digests + pin) must
be present at head unchanged and in the same relative order; report additions."""
import json, sys
from pathlib import Path
d = Path(sys.argv[1]); ok = True
for mode in ("sdk", "absent"):
    base = json.loads((d / f"base-{mode}.json").read_text())
    head = json.loads((d / f"head-{mode}.json").read_text())
    for kind in ("accepted", "mutations"):
        b = [tuple(r) for r in base[kind]]; h = [tuple(r) for r in head[kind]]
        prefix = h[:len(b)] == b
        missing = [r[0] for r in b if r not in h]
        added = [r[0] for r in h if r not in b]
        labels_dup = len({r[0] for r in h}) != len(h)
        print(f"{mode} {kind}: base {len(b)} head {len(h)}; base rows are head's unchanged prefix: {prefix}; "
              f"base rows missing/changed at head: {len(missing)}; added: {len(added)}; duplicate head labels: {labels_dup}")
        for l in added: print(f"    + {l}")
        ok &= prefix and not missing
print("RESULT", "NO BASE ROW CHANGED" if ok else "BASE ROW CHANGED")

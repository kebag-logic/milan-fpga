#!/usr/bin/env python3
"""artcmp.py <art-dir> <base-label> <cand-label>: per config and placement, the artifact files that differ."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
a = json.loads((root / sys.argv[2] / "receipt.json").read_text())
b = json.loads((root / sys.argv[3] / "receipt.json").read_text())
rc = 0
for key in sorted(set(a) | set(b)):
    fa, fb = a.get(key, {}).get("files", {}), b.get(key, {}).get("files", {})
    diff = sorted(n for n in set(fa) | set(fb) if fa.get(n) != fb.get(n))
    same = len(set(fa) & set(fb)) - len([n for n in diff if n in fa and n in fb])
    print(f"{key}: {'IDENTICAL' if not diff else 'DIFFERS'} ({same} equal of {len(fb)})"
          f" model {a.get(key, {}).get('model_id')} -> {b.get(key, {}).get('model_id')}"
          f" clusters_in {a.get(key, {}).get('clusters_in')} -> {b.get(key, {}).get('clusters_in')}")
    for n in diff:
        print(f"    {n}: {fa.get(n, {}).get('bytes')} -> {fb.get(n, {}).get('bytes')} B")
    if diff and "ax7101_8x8" not in key:
        rc = 1
print("RESULT:", "only the 8x8 differs" if rc == 0 else "A CONFIG OTHER THAN THE 8x8 DIFFERS")
sys.exit(rc)

#!/usr/bin/env python3
"""Compare two pp_resource_baseline.json blobs: report every changed leaf path,
classifying measured fields (figures, scopes, inputs_sha256, measured) vs all others."""
import json, subprocess, sys
repo, a, b = sys.argv[1:4]
def load(rev):
    return json.loads(subprocess.run(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"],
                                     check=True, capture_output=True).stdout)
def walk(x, p=()):
    if isinstance(x, dict):
        for k, v in x.items(): yield from walk(v, p + (str(k),))
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from walk(v, p + (str(i),))
    else: yield p, x
A, B = dict(walk(load(a))), dict(walk(load(b)))
MEASURED = ("figures", "scopes", "inputs_sha256", "measured")
other = []; measured = 0
for k in sorted(set(A) | set(B)):
    if A.get(k, "<absent>") != B.get(k, "<absent>"):
        if any(m in k for m in MEASURED): measured += 1
        else: other.append((k, A.get(k, "<absent>"), B.get(k, "<absent>")))
print(f"measured-field leaf changes: {measured}")
print(f"non-measured leaf changes: {len(other)}")
for o in other: print("  ", "/".join(o[0]), o[1], "->", o[2])
sys.exit(1 if other else 0)

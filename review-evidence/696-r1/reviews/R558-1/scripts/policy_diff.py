#!/usr/bin/env python3
"""Compare the resource baseline at two commits: which keys changed.

Usage: python3 -I policy_diff.py <repo> <old-commit> <new-commit>
Prints every changed leaf path; exits 1 if any policy leaf (tolerance,
floor, ceiling) or identity leaf changed, else 0.
"""
import json
import subprocess
import sys

repo, old, new = sys.argv[1:4]


def load(commit):
    out = subprocess.run(["git", "-C", repo, "show",
                          f"{commit}:syn/ooc/pp_resource_baseline.json"],
                         check=True, capture_output=True).stdout
    return json.loads(out)


def leaves(obj, path=()):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, obj


a = dict(leaves(load(old)))
b = dict(leaves(load(new)))
changed = sorted(set(a) | set(b), key=lambda p: p)
bad = 0
kinds = {}
for p in changed:
    if a.get(p, "<absent>") == b.get(p, "<absent>"):
        continue
    cls = "other"
    for tag in ("tolerance", "floor", "ceiling", "identity", "figures",
                "scopes", "inputs_sha256", "measured"):
        if tag in p:
            cls = tag
            break
    kinds[cls] = kinds.get(cls, 0) + 1
    if cls in ("tolerance", "floor", "ceiling", "identity", "other"):
        bad += 1
        print("POLICY/OTHER CHANGE", "/".join(p), a.get(p, "<absent>"), "->",
              b.get(p, "<absent>"))
print("changed leaves by class:", json.dumps(kinds, sort_keys=True))
for ep in load(new)["endpoints"] if "endpoints" in load(new) else []:
    pass
print("RESULT:", "POLICY CHANGED" if bad else "policy and identity unchanged")
sys.exit(1 if bad else 0)

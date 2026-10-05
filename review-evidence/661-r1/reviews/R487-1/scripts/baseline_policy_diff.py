#!/usr/bin/env python3
"""Compare pp_resource_baseline.json between two revisions: every non-figure field
(policy: tolerance, floors, ceilings, recipe/tool identity) must be equal; print the
changed paths so a reviewer sees exactly what a re-baseline moved.
Usage: baseline_policy_diff.py <repo> <base-rev> <head-rev>"""
import json, subprocess, sys
repo, base, head = sys.argv[1:4]
def load(rev):
    return json.loads(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:syn/ooc/pp_resource_baseline.json"]))
def flat(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, f"{p}[{i}]")
    else:
        yield p, o
a, b = dict(flat(load(base))), dict(flat(load(head)))
changed = sorted(k for k in a.keys() | b.keys() if a.get(k, "<absent>") != b.get(k, "<absent>"))
cats = {}
for k in changed:
    seg = k.split("/")
    cat = "figures" if "/figures/" in k else "scopes" if "/scopes/" in k else "/".join(s for s in seg[3:] if s) or k
    cats.setdefault(cat, []).append(k)
for cat, ks in sorted(cats.items()):
    print(f"CHANGED-CATEGORY {cat}: {len(ks)} path(s)")
    if cat not in ("figures", "scopes"):
        for k in ks:
            print(f"   {k}: {a.get(k, '<absent>')!r} -> {b.get(k, '<absent>')!r}")
print("ENDPOINTS", sorted(load(head)["endpoints"].keys()) if isinstance(load(head)["endpoints"], dict) else [e.get("name") for e in load(head)["endpoints"]])

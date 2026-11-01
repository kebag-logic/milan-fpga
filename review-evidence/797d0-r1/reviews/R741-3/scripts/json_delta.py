#!/usr/bin/env python3
"""Entry-level delta of scripts/docs_inventory.json between two commits. Usage: json_delta.py REPO OLD NEW"""
import json, subprocess, sys
repo, old, new = sys.argv[1:4]
def load(rev):
    return json.loads(subprocess.check_output(["git", "-C", repo, "show", f"{rev}:scripts/docs_inventory.json"], text=True))
a, b = load(old), load(new)
print("top keys", sorted(b), "verified_at", a.get("verified_at"), b.get("verified_at"), "cited_at", a.get("cited_at"), b.get("cited_at"))
A = {f["id"]: f for f in a["findings"]}; B = {f["id"]: f for f in b["findings"]}
print("counts", len(A), len(B))
print("removed", sorted(set(A) - set(B)))
print("added", sorted(set(B) - set(A)))
for i in sorted(B):
    if i not in A:
        print("\n== ADDED", i); [print(f"  {k}: {v}") for k, v in B[i].items() if k != "id"]
    elif A[i] != B[i]:
        keys = [k for k in B[i] if A[i].get(k) != B[i].get(k)]
        print("\n== CHANGED", i, keys, "page", B[i]["page"])
        for k in keys:
            print(f"  -{k}: {A[i].get(k)}"); print(f"  +{k}: {B[i].get(k)}")

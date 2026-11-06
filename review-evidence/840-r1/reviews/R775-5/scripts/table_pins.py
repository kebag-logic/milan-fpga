#!/usr/bin/env python3
"""Which paths does ci/image/command-table.json pin, and do pins for files the
merge changed still match? usage: table_pins.py <repo> <changed-file list>"""
import hashlib, json, os, sys
root, listing = sys.argv[1], sys.argv[2]
t = json.load(open(os.path.join(root, "ci/image/command-table.json")))
changed = set(open(listing).read().split())
hits = {}
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "/" + str(k))
            if isinstance(k, str) and k in changed: hits.setdefault(k, []).append((path, v))
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        for c in changed:
            if c in o: hits.setdefault(c, []).append((path, o[:120]))
walk(t)
print("top-level keys:", list(t)[:10] if isinstance(t, dict) else type(t))
print("changed files named by the table:", len(hits))
for c, rows in sorted(hits.items()):
    print(" ", c, "x", len(rows), "e.g.", str(rows[0])[:170])

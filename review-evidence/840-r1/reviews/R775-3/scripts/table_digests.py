#!/usr/bin/env python3
"""Compare declared script digests at two commits; reproduce the table bytes.

usage: table_digests.py <repo> <head> <dev>
Reads blobs through git so the check is independent of the working tree.
"""
import hashlib, json, subprocess, sys
repo, head, dev = sys.argv[1:4]
def show(rev, path):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None
def rows(table):
    found = {}
    def walk(node):
        if isinstance(node, dict):
            for key, val in node.items():
                if isinstance(val, dict) and "sha256" in val and "class" in val:
                    found[key] = val
                else:
                    walk(val)
        elif isinstance(node, list):
            for val in node:
                walk(val)
    walk(table)
    return found
def stale(rev):
    table = json.loads(show(rev, "ci/image/command-table.json"))
    out = {}
    decl = rows(table)
    for path, row in decl.items():
        blob = show(rev, path)
        if blob is None:
            out[path] = "missing"
        elif hashlib.sha256(blob).hexdigest() != row["sha256"]:
            out[path] = "stale"
    return out, decl
sh, dh = stale(head)
sd, dd = stale(dev)
print("declared rows head/dev:", len(dh), len(dd))
print("mismatches head/dev:", len(sh), len(sd))
print("added at head:", sorted(set(sh) - set(sd)))
print("removed at head:", sorted(set(sd) - set(sh)))
print("rows whose declared fields differ head vs dev:", sorted(k for k in dh if dh[k] != dd.get(k)))
print("rows only at head/dev:", sorted(set(dh) - set(dd)), sorted(set(dd) - set(dh)))
changed = subprocess.run(["git", "-C", repo, "diff", "--name-only", dev, head], capture_output=True, text=True).stdout.split()
print("PR files:", len(changed))
for path in changed:
    if path in dh:
        state = sh.get(path, "match")
        print(f"  pinned PR file {path}: head {state}; dev {sd.get(path, 'match')}")

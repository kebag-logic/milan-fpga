#!/usr/bin/env python3
"""Fetch blobs of the public evidence tree (read-only GitHub API) into a directory.
usage: fetch_evidence.py TREE_JSON OUTDIR PREFIX [PREFIX...]"""
import base64, json, os, subprocess, sys
tree, out, prefixes = sys.argv[1], sys.argv[2], sys.argv[3:]
items = [t for t in json.load(open(tree))["tree"]
         if t["type"] == "blob" and any(t["path"].startswith(p) for p in prefixes)]
for t in items:
    dst = os.path.join(out, t["path"])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    raw = subprocess.run(["gh", "api", f"repos/kebag-logic/milan-fpga/git/blobs/{t['sha']}"],
                         check=True, capture_output=True).stdout
    open(dst, "wb").write(base64.b64decode(json.loads(raw)["content"]))
    print(t["sha"], t["path"])

#!/usr/bin/env python3
"""Verify exact tracked blob bytes, executable modes, index and gitlinks."""
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
head = "60c911b92825a720044e78bed540752c7dd0368e"
tree = "356130401dbcb3a47184742b9f4973508f2b72eb"

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def entries(ref):
    result = {}
    for row in git("ls-tree", "-rz", ref).split(b"\0"):
        if not row:
            continue
        fields, name = row.split(b"\t", 1)
        mode, kind, blob = fields.decode().split()
        result[name.decode()] = (mode, kind, blob)
    return result

errors = []
expected = entries(head)
index = {}
for row in git("ls-files", "--stage", "-z").split(b"\0"):
    if row:
        fields, name = row.split(b"\t", 1)
        mode, blob, stage = fields.decode().split()
        index[name.decode()] = (mode, blob, stage)
for name, (mode, kind, blob) in expected.items():
    path = root / name
    if kind == "blob":
        actual = git("hash-object", "--no-filters", str(path)).decode().strip()
        actual_mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
        if actual != blob or actual_mode != mode:
            errors.append([name, "worktree bytes or mode differ"])
        if index.get(name) != (mode, blob, "0"):
            errors.append([name, "index differs"])
if set(index) != set(expected):
    errors.append("index path set differs")
actual_head = git("rev-parse", "HEAD").decode().strip()
actual_tree = git("rev-parse", "HEAD^{tree}").decode().strip()
if (actual_head, actual_tree) != (head, tree):
    errors.append("HEAD identity differs")
gitlinks = {ref: {name: blob for name, (mode, kind, blob) in entries(ref).items() if mode == "160000"} for ref in ("ae982af85ec97286bd35b39403926d8f0eaec81d", "625b001173fda5f6401af1dceaef8d8ab86f5ae9", head)}
status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
if status:
    errors.append("nonempty worktree status")
result = {"head": actual_head, "tree": actual_tree, "tracked_entries": len(expected), "blob_bytes_modes_and_index_equal": not errors, "gitlinks": gitlinks, "status": status, "errors": errors}
(packet / "receipts/checkout-final.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
raise SystemExit(bool(errors))

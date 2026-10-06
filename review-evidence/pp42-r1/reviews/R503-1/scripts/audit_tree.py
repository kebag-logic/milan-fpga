#!/usr/bin/env python3
"""Read-only exact-commit, tracked-byte, mode, index and submodule verification."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
expected = "72facc6d48807808e4d97a454a0ecceb2769ac9e"
expected_tree = "3274eac801f2ebb6b96ca031c12752a2a1b91bcc"

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
errors = []
records = []
links = []
for entry in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not entry:
        continue
    meta, path = entry.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    rel = os.fsdecode(path)
    p = root / rel
    if mode == "160000":
        subhead = subprocess.check_output(["git", "-C", str(p), "rev-parse", "HEAD"]).decode().strip()
        links.append({"path": rel, "expected": oid, "actual": subhead})
        if subhead != oid:
            errors.append(rel + ": gitlink mismatch")
        continue
    data = os.fsencode(os.readlink(p)) if mode == "120000" else p.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    actual_mode = "120000" if p.is_symlink() else "100755" if p.stat().st_mode & 0o111 else "100644"
    if actual != oid or actual_mode != mode:
        errors.append(rel + ": bytes or mode mismatch")
    records.append({"path": rel, "mode": mode, "blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
index_tree = git("write-tree").decode().strip()
if (head, tree, index_tree) != (expected, expected_tree, expected_tree):
    errors.append("HEAD/tree/index identity mismatch")
result = {"head": head, "tree": tree, "index_tree": index_tree, "tracked_files": len(records),
          "submodule_gitlinks": links, "status": git("status", "--porcelain=v1", "--untracked-files=all").decode(),
          "errors": errors, "files": records}
print(json.dumps(result, indent=2))
sys.exit(bool(errors))

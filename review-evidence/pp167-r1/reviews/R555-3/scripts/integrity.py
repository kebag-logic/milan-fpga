#!/usr/bin/env python3
"""Check tracked bytes, executable modes, index entries and gitlinks against HEAD."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("repo", type=Path)
p.add_argument("output", type=Path)
a = p.parse_args()
def git(*args):
    return subprocess.check_output(["git", "-C", str(a.repo), *args])
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
assert head == "bcbf382e5f4d17ccfd8ae75a80bbc45902c75b7d"
assert tree == "9a5bb28e18469943b28e1ece0194dc9693e0d5b7"
entries = []
expected_index = []
links = []
for record in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if not record:
        continue
    meta, rawpath = record.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    rel = os.fsdecode(rawpath)
    f = a.repo / rel
    expected_index.append(f"{mode} {oid} 0\t{rel}".encode())
    if mode == "160000":
        actual = subprocess.check_output(["git", "-C", str(f), "rev-parse", "HEAD"]).decode().strip()
        assert actual == oid, rel
        links.append({"path": rel, "expected": oid, "actual": actual})
        continue
    data = os.fsencode(os.readlink(f)) if mode == "120000" else f.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == oid, rel
    actualmode = "120000" if f.is_symlink() else "100755" if f.stat().st_mode & 0o111 else "100644"
    assert actualmode == mode, (rel, mode, actualmode)
    entries.append({"path": rel, "mode": mode, "blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
assert git("ls-files", "--stage", "-z").split(b"\0")[:-1] == expected_index
status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
assert not status, status
out = {"head": head, "tree": tree, "status": status, "tracked_blobs": len(entries),
       "gitlinks": links, "index_matches_head": True, "files": entries}
a.output.write_text(json.dumps(out, indent=2) + "\n")
print(f"PASS: {len(entries)} tracked blobs/modes; index and HEAD match; {len(links)} gitlinks; clean worktree")

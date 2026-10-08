#!/usr/bin/env python3
"""Prove raw tracked bytes, executable modes, index and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
expected = "85db353400c6bf3965d279a9f5b5d47e08a0d1ed"
def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])
def audit(root, commit):
    entries = git(root, "ls-tree", "-rz", commit).split(b"\0")
    wanted_index = []
    bad = []
    blobs = 0
    links = {}
    for entry in filter(None, entries):
        meta, rawpath = entry.split(b"\t", 1)
        mode, kind, oid = meta.split()
        rel = os.fsdecode(rawpath)
        path = root / rel
        wanted_index.append(mode + b" " + oid + b" 0\t" + rawpath)
        if kind == b"commit":
            links[rel] = oid.decode()
            continue
        if mode == b"120000":
            data = os.fsencode(os.readlink(path)) if path.is_symlink() else b""
            okay_mode = path.is_symlink()
        else:
            data = path.read_bytes() if path.is_file() else b""
            okay_mode = path.is_file() and not path.is_symlink() and bool(path.stat().st_mode & 0o111) == (mode == b"100755")
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if digest != oid.decode() or not okay_mode:
            bad.append(rel)
        blobs += 1
    actual_index = list(filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")))
    assert sorted(actual_index) == sorted(wanted_index), "index differs from commit"
    assert not bad, bad
    assert git(root, "rev-parse", "HEAD").decode().strip() == commit
    return {"head": commit, "tree": git(root, "rev-parse", commit + "^{tree}").decode().strip(), "tracked_blobs_checked": blobs, "bytes_modes_index": "PASS", "gitlinks": links}

record = {"root": audit(repo, expected), "submodules": {}}
for name in ("third_party/verilog-axis", "protocol-processor", "gptp-processor"):
    record["submodules"][name] = audit(repo / name, record["root"]["gitlinks"][name])
lane, dev, merge = "2525eae9", "99e4eb6c", "9a0d68e20"
base = git(repo, "merge-base", lane, dev).decode().strip()
paths = lambda a, b: set(git(repo, "diff", "--name-only", a, b).decode().splitlines())
left, right = paths(base, lane), paths(base, dev)
assert not left & right
for ancestor, names in ((lane, left), (dev, right)):
    assert not names & paths(ancestor, merge)
assert not git(repo, "show", "--remerge-diff", "--format=", merge)
record["composition"] = {"base": base, "lane_paths": len(left), "incoming_dev_paths": len(right), "overlap": [], "lane_and_dev_entries_retained": "PASS", "remerge_diff": "empty", "post_merge_paths": sorted(paths(merge, expected))}
print(json.dumps(record, indent=2))

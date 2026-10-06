#!/usr/bin/env python3
"""Check committed bytes, file modes, indexes and required gitlinks directly."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("receipt", type=Path)
a = p.parse_args()
root = a.repository.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
expected = "a27808375427859dc357f6bfd0a88842062b20ed"
expected_tree = "5519813ecda9827ba2f30a15ede5aa9e66bc4bea"
required = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], env=env)

def inspect(repo, revision):
    entries = {}
    links = {}
    errors = []
    blobs = 0
    for record in git(repo, "ls-tree", "-rz", revision).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        entries[path] = (mode, oid)
        if kind == b"commit":
            links[os.fsdecode(path)] = oid.decode()
            continue
        name = repo / os.fsdecode(path)
        try:
            info = name.lstat()
            if mode == b"120000":
                assert stat.S_ISLNK(info.st_mode)
                data = os.fsencode(os.readlink(name))
            else:
                assert stat.S_ISREG(info.st_mode)
                actual_mode = b"100755" if info.st_mode & 0o111 else b"100644"
                assert actual_mode == mode
                data = name.read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert actual == oid.decode()
            blobs += 1
        except (OSError, AssertionError):
            errors.append("bytes/mode: " + os.fsdecode(path))
    indexed = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        if stage != b"0" or path in indexed:
            errors.append("unmerged/duplicate index: " + os.fsdecode(path))
        indexed[path] = (mode, oid)
    if entries != indexed:
        errors.append("index differs from committed tree")
    for record in git(repo, "ls-files", "-v", "-z").split(b"\0"):
        if record and (record[:1].islower() or record[:1] == b"S"):
            errors.append("hidden index flag: " + os.fsdecode(record[2:]))
    actual_head = git(repo, "rev-parse", "HEAD").decode().strip()
    if actual_head != revision:
        errors.append("HEAD differs from expected revision")
    return dict(head=actual_head, tree=git(repo, "rev-parse", revision + "^{tree}").decode().strip(),
                tracked_blobs_verified=blobs, index_entries=len(indexed), gitlinks=links,
                errors=errors)

results = {"root": inspect(root, expected)}
assert results["root"]["tree"] == expected_tree
for path in required:
    pin = results["root"]["gitlinks"][path]
    assert (root / path / ".git").is_file(), "required registered submodule missing"
    results[path] = inspect(root / path, pin)
results["external_note"] = "Unused external gitlink verified in root tree/index; checkout uninitialized."
results["pass"] = all(not r["errors"] for r in results.values() if isinstance(r, dict))
a.receipt.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
raise SystemExit(0 if results["pass"] else 1)

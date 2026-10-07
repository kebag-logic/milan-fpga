#!/usr/bin/env python3
"""Read-only exact-byte, mode, index and gitlink audit from the candidate cwd."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "fe8294978dd306706d659dc06468d0c07d43ce3e"
TREE = "1d9982e2943098fd1003e069dc7df8cc210d98ca"
PRIOR = "5428b044176f95248e6916dc00dd89c0df154078"
BASE = "e21c1ca024d37ea188ad15b5c8f9c2dae18628df"
ROOT = Path.cwd()
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(*args, root=ROOT):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)

def entries(rev, root=ROOT):
    rows = {}
    for row in git("ls-tree", "-rz", rev, root=root).split(b"\0"):
        if row:
            metadata, path = row.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            rows[os.fsdecode(path)] = (mode, oid)
    return rows

def check_checkout(root, expected, label):
    assert git("rev-parse", "HEAD", root=root).decode().strip() == expected
    assert Path(git("rev-parse", "--show-toplevel", root=root).decode().strip()).resolve() == root.resolve()
    tree = entries(expected, root)
    index = {}
    for row in git("ls-files", "--stage", "-z", root=root).split(b"\0"):
        if row:
            metadata, path = row.split(b"\t", 1)
            mode, oid, stage = metadata.decode().split()
            assert stage == "0", (label, path, stage)
            assert os.fsdecode(path) not in index
            index[os.fsdecode(path)] = (mode, oid)
    assert index == tree, (label, "index differs from committed tree")
    fingerprints = []
    links = {}
    for path, (mode, oid) in sorted(tree.items()):
        if mode == "160000":
            links[path] = oid
            continue
        physical = root / path
        info = physical.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), (label, path, "not a symlink")
            data = os.fsencode(os.readlink(physical))
        else:
            assert stat.S_ISREG(info.st_mode), (label, path, "not regular")
            actual_mode = "100755" if info.st_mode & 0o111 else "100644"
            assert mode == actual_mode, (label, path, "mode mismatch")
            data = physical.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert oid == actual, (label, path, "blob mismatch")
        fingerprints.append(f"{mode} {actual} {path}\n")
    return dict(checkout=label, head=expected, tracked_entries=len(tree),
                verified_blobs=len(fingerprints), index_matches=True,
                bytes_and_modes_match=True, gitlinks=links,
                blob_census_sha256=hashlib.sha256("".join(fingerprints).encode()).hexdigest(),
                status=git("status", "--porcelain=v1", "--untracked-files=all", root=root).decode())

assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
current, prior = entries(HEAD), entries(PRIOR)
changes = sorted(path for path in set(current) | set(prior) if current.get(path) != prior.get(path))
assert changes == ["CHANGELOG.md", "docs/reference/SUBMODULES.md", "docs/testing/PP_SHADOW_BASELINE_RECIPE.md"]
results = [check_checkout(ROOT, HEAD, "parent")]
for path in ["protocol-processor", "gptp-processor", "third_party/verilog-axis"]:
    results.append(check_checkout(ROOT / path, current[path][1], path))
for result in results:
    assert not result["status"], (result["checkout"], result["status"])
unchanged_scopes = ["sw/firmware/milan_baremetal", "tb/verilator/nvm_capture_cpu", "hdl", "configs"]
for scope in unchanged_scopes:
    assert not git("diff", "--name-only", BASE, HEAD, "--", scope), scope
result = dict(head=HEAD, tree=TREE, base=BASE, prior=PRIOR,
              changed_since_prior=changes,
              all_other_entries_identical=True,
              unchanged_from_source_base=unchanged_scopes,
              checkouts=results,
              unused_external="gitlink verified; historical unused checkout remains uninitialized")
print(json.dumps(result, indent=2))

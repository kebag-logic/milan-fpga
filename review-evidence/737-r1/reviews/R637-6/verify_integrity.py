#!/usr/bin/env python3
"""Verify tracked bytes, types, executable modes, indexes and dependency gitlinks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("packet", type=Path)
a = ap.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, env=env)

def audit(root, revision):
    tree = git(root, "ls-tree", "-rz", revision).split(b"\0")
    expected, blobs, links, errors = {}, 0, {}, []
    for line in filter(None, tree):
        info, name = line.split(b"\t", 1)
        mode, kind, oid = info.split()
        expected[name] = (mode, oid, b"0")
        path = root / os.fsdecode(name)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        try:
            st = path.lstat()
            if mode == b"120000":
                assert stat.S_ISLNK(st.st_mode)
                data = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(st.st_mode)
                assert bool(st.st_mode & 0o111) == (mode == b"100755")
                data = path.read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert actual == oid.decode()
            blobs += 1
        except (OSError, AssertionError):
            errors.append(os.fsdecode(name))
    index = {}
    for line in filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")):
        info, name = line.split(b"\t", 1)
        mode, oid, stage = info.split()
        assert name not in index, "unmerged index"
        index[name] = (mode, oid, stage)
    assert index == expected, "index differs from committed tree"
    assert not errors, errors
    return dict(blobs=blobs, gitlinks=links, index_matches=True, bytes_types_modes_match=True)

head = git(repo, "rev-parse", "HEAD").decode().strip()
assert head == "47fd0d3c510000e9412a1613a723b61d4ef2ae4a"
tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
assert tree == "771055d82f5b90249c2610a6a20f1be36b15bf56"
root = audit(repo, head)
deps = {}
for name in ("protocol-processor", "gptp-processor", "third_party/verilog-axis",
             "third_party/tsn-c-stack", "third_party/lwSRP"):
    path = repo / name
    pin = root["gitlinks"][name]
    assert not path.is_symlink() and (path / ".git").is_file()
    assert git(path, "rev-parse", "HEAD").decode().strip() == pin
    assert Path(git(path, "rev-parse", "--show-superproject-working-tree").decode().strip()).resolve() == repo
    deps[name] = dict(pin=pin, **audit(path, pin))
runner = hashlib.sha256((repo / "scripts/act_ci.py").read_bytes()).hexdigest()
prior = hashlib.sha256(git(repo, "show", "e3d25d96:scripts/act_ci.py")).hexdigest()
assert runner == prior == "f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c"
delta = git(repo, "diff", "--name-only", "e3d25d96", head).decode().splitlines()
assert not any(n.startswith(("hdl/", "sw/")) for n in delta)
out = dict(head=head, tree=tree, root=root, dependencies=deps,
           runner_sha256=runner, runner_unchanged=True, delta_paths=delta,
           product_code_delta=False, status=git(repo, "status", "--short").decode(),
           unused_external="Uninitialized; recorded gitlink checked in root index/tree.")
(packet / "receipts/checkout-integrity.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))

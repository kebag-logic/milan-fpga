#!/usr/bin/env python3
"""R924: prove tracked bytes, modes, index entries and initialized gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve()
ENV = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}
HEAD = "9c62539365fea8316dae2b9fd7c68defeff5cb31"
TREE = "bbbe38c7db0b82682798e8afb1feb3a41a4ff491"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack", "third_party/lwSRP")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], env=ENV)


def audit(root, rev):
    records = git(root, "ls-tree", "-rz", "--full-tree", rev).split(b"\0")
    tree, links, errors = {}, {}, []
    for record in filter(None, records):
        header, name = record.split(b"\t", 1)
        mode, kind, oid = header.split()
        tree[name] = (mode, oid)
        path = root / os.fsdecode(name)
        if kind == b"commit":
            links[os.fsdecode(name)] = oid.decode()
            continue
        try:
            info = path.lstat()
            if mode == b"120000":
                assert stat.S_ISLNK(info.st_mode)
                data = os.fsencode(os.readlink(path))
            else:
                assert stat.S_ISREG(info.st_mode)
                assert bool(info.st_mode & 0o111) == (mode == b"100755")
                data = path.read_bytes()
            actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            assert actual == oid.decode()
        except (OSError, AssertionError):
            errors.append(os.fsdecode(name))
    index = {}
    for record in filter(None, git(root, "ls-files", "--stage", "-z").split(b"\0")):
        header, name = record.split(b"\t", 1)
        mode, oid, stage = header.split()
        assert stage == b"0", (name, stage)
        assert name not in index
        index[name] = (mode, oid)
    assert index == tree, "index differs from commit tree"
    assert not errors, errors
    return {"tracked_entries": len(tree), "bytes_modes_index_exact": True, "gitlinks": links}


def main():
    assert git(ROOT, "rev-parse", "HEAD").decode().strip() == HEAD
    assert git(ROOT, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
    result = {"reviewer": "R924", "head": HEAD, "tree": TREE, "superproject": audit(ROOT, HEAD), "submodules": {}}
    for name in REQUIRED:
        path = ROOT / name
        assert (path / ".git").is_file(), name
        assert git(path, "rev-parse", "--show-superproject-working-tree").decode().strip() == str(ROOT)
        pin = result["superproject"]["gitlinks"][name]
        assert git(path, "rev-parse", "HEAD").decode().strip() == pin
        result["submodules"][name] = {"head": pin, **audit(path, pin)}
    result["status_porcelain"] = git(ROOT, "status", "--porcelain=v1", "--untracked-files=no").decode()
    assert result["status_porcelain"] == ""
    result["full_delta_paths"] = git(ROOT, "diff", "--name-only", "fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f", HEAD).decode().splitlines()
    assert not any(Path(p).suffix in (".sv", ".v", ".c", ".cpp", ".h") for p in result["full_delta_paths"])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

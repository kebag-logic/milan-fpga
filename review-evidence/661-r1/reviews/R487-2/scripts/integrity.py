#!/usr/bin/env python3
"""Prove tracked bytes, file modes, index entries and required gitlinks."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "3880c1eb6e2f927a07f98150d5b05a228f8f4efd"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args],
                                   env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})


def prove(root, expected, recurse=False):
    assert git(root, "rev-parse", "HEAD").decode().strip() == expected
    tree = git(root, "ls-tree", "-rz", "--full-tree", expected)
    entries = []
    links = {}
    for record in tree.split(b"\0"):
        if not record:
            continue
        meta, raw = record.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        name = os.fsdecode(raw)
        entries.append(mode.encode() + b" " + oid.encode() + b" 0\t" + raw + b"\0")
        path = root / name
        if kind == "commit":
            links[name] = oid
            continue
        info = path.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual = "100755" if info.st_mode & 0o111 else "100644"
            assert mode == actual, (name, mode, actual)
            data = path.read_bytes()
        got = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert got == oid, (name, got, oid)
    index = git(root, "ls-files", "--stage", "-z")
    assert index == b"".join(entries), "index differs from exact tree"
    result = {"head": expected, "tree": git(root, "rev-parse", "HEAD^{tree}").decode().strip(),
              "tracked_entries": len(entries), "tracked_bytes_modes_index": "PASS", "gitlinks": links}
    if recurse:
        result["required_submodules"] = {}
        for name in REQUIRED:
            sub = root / name
            assert sub.is_dir() and not sub.is_symlink() and (sub / ".git").is_file(), name
            owner = git(sub, "rev-parse", "--show-superproject-working-tree").decode().strip()
            assert Path(owner).resolve() == root.resolve(), name
            result["required_submodules"][name] = prove(sub, links[name])
    return result


if __name__ == "__main__":
    print(json.dumps(prove(Path(sys.argv[1]).resolve(), HEAD, True), indent=2))

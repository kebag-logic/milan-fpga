#!/usr/bin/env python3
"""Prove exact tracked bytes, modes, index records and required gitlinks.

Usage: python3 verify_checkout.py CHECKOUT
Reads pinned trees, never uses status flags as a byte-equality proof.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "bef8dd7036f711bf286929fa4cba6bf724c7118d"
TREE = "20594912f6c5e614d2686232569402d6b48a2473"
BASE = "fa450d301805881ad713b67521477bf042ddadfd"
REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")


def git(repo, *args):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
    return subprocess.check_output(["git", "-C", str(repo), *args], env=env)


def verify(repo, revision):
    assert git(repo, "rev-parse", "HEAD").decode().strip() == revision
    tree = {}
    for row in git(repo, "ls-tree", "-rz", revision).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, kind, oid = meta.decode().split()
            tree[os.fsdecode(name)] = (mode, kind, oid)
    index = {}
    for row in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, oid, stage = meta.decode().split()
            assert stage == "0"
            index[os.fsdecode(name)] = (mode, oid)
    assert index == {name: (m, oid) for name, (m, _, oid) in tree.items()}
    checked = 0
    for name, (mode, kind, oid) in tree.items():
        if kind == "commit":
            continue
        p = repo / name
        st = p.lstat()
        if mode == "120000":
            assert stat.S_ISLNK(st.st_mode)
            data = os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(st.st_mode)
            assert bool(st.st_mode & 0o111) == (mode == "100755")
            data = p.read_bytes()
        measured = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert measured == oid, name
        checked += 1
    return tree, checked


def main():
    repo = Path(sys.argv[1]).resolve()
    assert git(repo, "rev-parse", "HEAD^{tree}").decode().strip() == TREE
    tree, checked = verify(repo, HEAD)
    print(json.dumps({"role": "parent", "head": HEAD, "tree": TREE, "verified_blobs": checked, "index_and_modes": "equal"}))
    for name in REQUIRED:
        mode, kind, pin = tree[name]
        assert mode == "160000" and kind == "commit"
        assert not (repo / name).is_symlink()
        assert (repo / name / ".git").is_file()
        _, count = verify(repo / name, pin)
        print(json.dumps({"role": name, "gitlink": pin, "verified_blobs": count, "index_and_modes": "equal"}))
    diff = git(repo, "diff", "--name-only", BASE, HEAD).decode().splitlines()
    assert diff == ["docs/findings/653_DISCONNECT_ORDER_BENCH.md"]
    assert not git(repo, "diff", "--raw", BASE, HEAD, "--", "hdl", "sw", *REQUIRED)
    print(json.dumps({"changed_paths": diff, "source_and_gitlinks_unchanged": True,
                      "untracked_files": len(git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")) - 1,
                      "result": "PASS"}))


if __name__ == "__main__":
    main()

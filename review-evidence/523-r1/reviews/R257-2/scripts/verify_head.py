#!/usr/bin/env python3
"""Verify the review clone is exactly the published head: commit, tree, index,
tracked blob bytes and modes on disk, and the required submodule gitlinks.

Usage: verify_head.py CLONE EXPECTED_HEAD EXPECTED_TREE
Prints one JSON object; exit 0 only when every check holds.
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

REQUIRED = ("gptp-processor", "protocol-processor", "third_party/verilog-axis")


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "--no-replace-objects", "--no-optional-locks", "-C", str(root), *args],
                          env=env, capture_output=True, check=True).stdout


def blob_id(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_tree(root, revision):
    """Compare every committed entry at `revision` with the index and disk."""
    tree = {}
    for row in git(root, "ls-tree", "-rz", "--full-tree", revision).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, _kind, obj = meta.decode().split(" ")
            tree[os.fsdecode(name)] = (mode, obj)
    index = {}
    for row in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, obj, stage = meta.decode().split(" ")
            index[os.fsdecode(name)] = (mode, obj, stage)
    problems = []
    if set(tree) != set(index):
        problems.append(["index-population", sorted(set(tree) ^ set(index))[:20]])
    for name, (mode, obj) in tree.items():
        ix = index.get(name)
        if ix is None or ix != (mode, obj, "0"):
            problems.append(["index-record", name, ix, (mode, obj)])
            continue
        path = Path(root) / name
        if mode == "160000":
            continue
        try:
            info = path.lstat()
        except FileNotFoundError:
            problems.append(["missing", name])
            continue
        if mode == "120000":
            ok = stat.S_ISLNK(info.st_mode) and blob_id(os.readlink(path).encode()) == obj
        else:
            ok = (stat.S_ISREG(info.st_mode) and blob_id(path.read_bytes()) == obj
                  and bool(info.st_mode & stat.S_IXUSR) == (mode == "100755"))
        if not ok:
            problems.append(["bytes-or-mode", name])
    return len(tree), problems


def main():
    clone, head, tree_id = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    result = {"clone": clone.name}
    result["head"] = git(clone, "rev-parse", "HEAD").decode().strip()
    result["tree"] = git(clone, "rev-parse", "HEAD^{tree}").decode().strip()
    count, problems = verify_tree(clone, "HEAD")
    result["tracked_entries"] = count
    result["problems"] = problems
    status = git(clone, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--ignore-submodules=none")
    result["status_entries"] = [os.fsdecode(r) for r in status.split(b"\0") if r]
    subs = {}
    for name in REQUIRED:
        pin = git(clone, "ls-tree", "HEAD", "--", name).decode().split()[2]
        path = clone / name
        actual = git(path, "rev-parse", "HEAD").decode().strip()
        top = git(path, "rev-parse", "--show-toplevel").decode().strip()
        n, p = verify_tree(path, pin)
        subs[name] = {"pin": pin, "checkout": actual, "own_toplevel": Path(top) == path,
                      "tracked_entries": n, "problems": p}
    result["submodules"] = subs
    ok = (result["head"] == head and result["tree"] == tree_id and not problems
          and not result["status_entries"]
          and all(s["pin"] == s["checkout"] and s["own_toplevel"] and not s["problems"] for s in subs.values()))
    result["verdict"] = "EXACT" if ok else "MISMATCH"
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

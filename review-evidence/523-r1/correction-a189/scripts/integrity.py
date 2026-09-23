#!/usr/bin/env python3
"""Snapshot a checkout: HEAD, tree, index flags, every tracked blob/mode on disk, and gitlinks.

Usage: integrity.py CHECKOUT OUT.json
Verifies that every index entry's worktree bytes hash to the recorded blob, that
modes match, that no entry carries assume-unchanged/skip-worktree, that the index
equals HEAD's tree, and that the three required submodules sit at their gitlinks
with clean trees. Exit 0 = clean; 1 = a discrepancy (listed in the JSON).
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REQUIRED = ("gptp-processor", "protocol-processor", "third_party/verilog-axis")


def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "--no-replace-objects", "--no-optional-locks", "-C", str(root), *args],
                          env=env, check=True, capture_output=True).stdout


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check(root):
    problems = []
    head = git(root, "rev-parse", "HEAD").decode().strip()
    tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
    flags = git(root, "ls-files", "-v", "-z").split(b"\0")
    odd = [f.decode(errors="replace") for f in flags if f and f[:1] not in (b"H",)]
    if odd:
        problems.append(["index flags", odd[:20]])
    staged = git(root, "ls-files", "--stage", "-z").split(b"\0")
    headrows = {}
    for row in git(root, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, _kind, obj = meta.split()
            headrows[name] = (mode, obj)
    files = 0
    gitlinks = {}
    seen = set()
    for row in staged:
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, obj, stage = meta.split()
        seen.add(name)
        if stage != b"0":
            problems.append(["unmerged", name.decode()])
        if headrows.get(name) != (mode, obj):
            problems.append(["index differs from HEAD", name.decode()])
        path = root / os.fsdecode(name)
        if mode == b"160000":
            gitlinks[name.decode()] = obj.decode()
            continue
        files += 1
        if mode == b"120000":
            data = os.readlink(path).encode() if path.is_symlink() else None
        else:
            data = path.read_bytes() if path.is_file() and not path.is_symlink() else None
        if data is None or blob(data) != obj.decode():
            problems.append(["bytes", name.decode()])
            continue
        if mode in (b"100644", b"100755"):
            exe = bool(path.lstat().st_mode & 0o100)
            if exe != (mode == b"100755"):
                problems.append(["mode", name.decode()])
    missing = set(headrows) - seen
    if missing:
        problems.append(["missing from index", sorted(m.decode() for m in missing)[:20]])
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    untracked = [u.decode(errors="replace") for u in untracked if u]
    if untracked:
        problems.append(["untracked", untracked[:20]])
    return dict(head=head, tree=tree, tracked_files=files, gitlinks=gitlinks,
                problems=problems)


def main():
    root = Path(sys.argv[1]).resolve()
    result = check(root)
    subs = {}
    for name in REQUIRED:
        sub = root / name
        try:
            sub_head = git(sub, "rev-parse", "HEAD").decode().strip()
            sub_result = check(sub)
        except subprocess.CalledProcessError as exc:
            result["problems"].append(["submodule unreadable", name, exc.returncode])
            continue
        if sub_head != result["gitlinks"].get(name):
            result["problems"].append(["submodule off pin", name, sub_head])
        if sub_result["problems"]:
            result["problems"].append(["submodule dirty", name, sub_result["problems"]])
        subs[name] = dict(head=sub_head, tree=sub_result["tree"], tracked_files=sub_result["tracked_files"])
    result["submodules"] = subs
    result["verdict"] = "CLEAN" if not result["problems"] else "DISCREPANCY"
    Path(sys.argv[2]).write_text(json.dumps(result, indent=1) + "\n")
    print(f"{result['verdict']}: head {result['head']} tree {result['tree']} files {result['tracked_files']} "
          f"gitlinks {result['gitlinks']} problems {len(result['problems'])}")
    return 0 if not result["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())

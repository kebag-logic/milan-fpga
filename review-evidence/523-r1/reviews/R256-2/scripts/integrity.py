#!/usr/bin/env python3
"""Reviewer receipt: prove a checkout's tracked bytes/modes/index and required gitlinks.

Usage: integrity.py REPO EXPECTED_HEAD
Every tracked regular file and symlink is hashed from disk as a Git blob and
compared with its index record and with HEAD's tree; modes are compared too.
Required submodules must be checked out exactly at their gitlinks.
"""
import hashlib, os, stat, subprocess, sys
from pathlib import Path

def git(root, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.check_output(["git", "--no-replace-objects", "--no-optional-locks", "-C", str(root), *args], env=env)

def records(text, tree):
    out = {}
    for row in text.split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        a, b, c = meta.split()
        out[name.decode()] = (a.decode(), (c if tree else b).decode(), None if tree else c.decode())
    return out

def check(root, rev):
    problems = []
    head = git(root, "rev-parse", "HEAD").strip().decode()
    if rev and head != rev:
        problems.append(f"HEAD {head} != {rev}")
    tree = records(git(root, "ls-tree", "-rz", "HEAD"), True)
    index = records(git(root, "ls-files", "--stage", "-z"), False)
    if set(tree) != set(index):
        problems.append(f"index/tree path sets differ: {sorted(set(tree) ^ set(index))[:5]}")
    count = 0
    for name, (mode, obj, stage) in index.items():
        if stage != "0":
            problems.append(f"unmerged {name}")
        if tree.get(name, (None, None))[:2] != (mode, obj):
            problems.append(f"index differs from HEAD: {name}")
        path = root / name
        if mode == "160000":
            continue
        try:
            info = path.lstat()
        except FileNotFoundError:
            problems.append(f"missing {name}")
            continue
        if mode == "120000":
            if not stat.S_ISLNK(info.st_mode):
                problems.append(f"not a symlink {name}")
                continue
            data = os.readlink(path).encode()
        else:
            if not stat.S_ISREG(info.st_mode):
                problems.append(f"not regular {name}")
                continue
            data = path.read_bytes()
            if bool(info.st_mode & stat.S_IXUSR) != (mode == "100755"):
                problems.append(f"mode {oct(info.st_mode)} != {mode}: {name}")
        blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if blob != obj:
            problems.append(f"bytes differ: {name}")
        count += 1
    flags = git(root, "ls-files", "-v", "-z").split(b"\0")
    hidden = [f.decode() for f in flags if f and (f[:1].islower() or f[:1] == b"S")]
    if hidden:
        problems.append(f"assume-unchanged/skip-worktree flags: {hidden[:5]}")
    status = git(root, "status", "--porcelain=v1", "--ignore-submodules=none", "-uall").decode()
    return head, count, problems, status, index

def main():
    root = Path(sys.argv[1]).resolve()
    rev = sys.argv[2] if len(sys.argv) > 2 else ""
    head, count, problems, status, index = check(root, rev)
    print(f"HEAD {head}")
    print(f"tree {git(root, 'rev-parse', 'HEAD^{tree}').strip().decode()}")
    print(f"tracked files hashed: {count}")
    print("index sha256 " + hashlib.sha256(git(root, "ls-files", "--stage", "-z")).hexdigest())
    for sub in ("gptp-processor", "protocol-processor", "third_party/verilog-axis"):
        pin = index[sub]
        actual = git(root / sub, "rev-parse", "HEAD").strip().decode()
        top = Path(git(root / sub, "rev-parse", "--show-toplevel").strip().decode())
        ok = pin[0] == "160000" and actual == pin[1] and top == root / sub
        if not ok:
            problems.append(f"submodule {sub} pin {pin} actual {actual} top {top}")
        sub_head, sub_count, sub_problems, sub_status, _ = check(root / sub, pin[1])
        problems += [f"{sub}: {p}" for p in sub_problems]
        if sub_status.strip():
            problems.append(f"{sub}: status not clean: {sub_status.strip()[:200]}")
        print(f"submodule {sub} gitlink {pin[1]} checkout {actual} files {sub_count} {'OK' if ok and not sub_problems else 'BAD'}")
    print("status porcelain (untracked+tracked): " + (repr(status) if status else "clean"))
    for p in problems:
        print("PROBLEM " + p)
    print("INTEGRITY " + ("OK" if not problems and not status else "FAIL"))
    return 0 if not problems and not status else 1

if __name__ == "__main__":
    sys.exit(main())

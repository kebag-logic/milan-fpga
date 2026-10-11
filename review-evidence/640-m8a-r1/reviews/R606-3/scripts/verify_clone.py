#!/usr/bin/env python3
"""R606-3: verify a checkout's tracked bytes, modes, index and gitlinks against an exact head.

usage: verify_clone.py <checkout> <head-sha> <tree-sha>
"""
import os
import stat
import subprocess
import sys
from pathlib import Path

repo, head, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]


def git(*args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


problems = []
if git("rev-parse", "HEAD").strip() != head:
    problems.append("HEAD differs")
if git("rev-parse", "HEAD^{tree}").strip() != tree:
    problems.append("HEAD tree differs")
if git("write-tree").strip() != tree:
    problems.append("index tree differs")
entries = [line.split(None, 3) for line in git("ls-files", "-s", "-z").split("\0") if line]
files = gitlinks = 0
for mode, oid, _stage, path in entries:
    p = repo / path
    if mode == "160000":
        gitlinks += 1
        if p.is_dir() and (p / ".git").exists():
            sub = subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            if sub != oid:
                problems.append(f"gitlink {path}: checked out {sub}, recorded {oid}")
        print(f"gitlink {path} {oid} {'populated' if (p / '.git').exists() else 'unpopulated'}")
        continue
    files += 1
    if mode == "120000":
        actual = git("hash-object", "--stdin", "-t", "blob") if False else None
        target = os.readlink(p).encode()
        got = subprocess.run(["git", "hash-object", "--stdin"], input=target, capture_output=True).stdout.decode().strip()
    else:
        got = subprocess.run(["git", "hash-object", "--no-filters", str(p)], capture_output=True, text=True).stdout.strip()
        want_exec = mode == "100755"
        if bool(p.stat().st_mode & stat.S_IXUSR) != want_exec:
            problems.append(f"mode {path}")
    if got != oid:
        problems.append(f"bytes {path}")
status = git("status", "--porcelain", "--untracked-files=all")
if status.strip():
    problems.append("status not empty: " + status[:400])
print(f"tracked files {files}, gitlinks {gitlinks}, problems {len(problems)}")
for p in problems:
    print("PROBLEM", p)
sys.exit(1 if problems else 0)

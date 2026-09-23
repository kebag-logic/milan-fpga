#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-3 final integrity of the review clone at the exact head.

Usage: r228_integrity.py <clone> <expected-head>

Checks, without trusting `git status` alone: HEAD and its tree; the index
equals HEAD (paths, modes, blob ids, stage 0 only); no assume-unchanged or
skip-worktree flag; every tracked regular file and symlink on disk hashes to
its index blob with the index mode; no untracked or ignored-but-present
extras outside .git; and each required submodule checkout is exactly at its
gitlink with a clean worktree.
"""

import os
import stat
import subprocess
import sys
from pathlib import Path

clone, expected = Path(sys.argv[1]), sys.argv[2]
env = {**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}


def git(*args, cwd=clone):
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                          capture_output=True, text=True).stdout


failures = []
head = git("rev-parse", "HEAD").strip()
tree = git("rev-parse", "HEAD^{tree}").strip()
if head != expected:
    failures.append(f"HEAD {head} != {expected}")
index = {}
for line in git("ls-files", "-s", "-z").split("\0"):
    if not line:
        continue
    meta, path = line.split("\t", 1)
    mode, blob, stage = meta.split()
    if stage != "0":
        failures.append(f"unmerged stage {stage}: {path}")
    index[path] = (mode, blob)
tracked = {}
for line in git("ls-tree", "-r", "-z", "HEAD").split("\0"):
    if not line:
        continue
    meta, path = line.split("\t", 1)
    mode, _kind, blob = meta.split()
    tracked[path] = (mode, blob)
if index != tracked:
    failures.append("index differs from HEAD tree")
flags = [line for line in git("ls-files", "-v").splitlines() if line[:2] != "H "]
if flags:
    failures.append(f"index flags present: {flags[:5]}")
checked = 0
for path, (mode, blob) in index.items():
    full = clone / path
    if mode == "160000":
        continue
    st = full.lstat()
    if mode == "120000":
        ok = stat.S_ISLNK(st.st_mode)
        data = os.readlink(full).encode()
        actual = subprocess.run(["git", "hash-object", "--stdin"], input=data,
                                cwd=clone, env=env, check=True,
                                capture_output=True).stdout.decode().strip()
    else:
        ok = stat.S_ISREG(st.st_mode) and \
            (mode == "100755") == bool(st.st_mode & stat.S_IXUSR)
        actual = git("hash-object", "--no-filters", "--", path).strip()
    if not ok or actual != blob:
        failures.append(f"byte/mode mismatch: {path}")
    checked += 1
extras = git("status", "--porcelain", "--ignored", "--untracked-files=all").strip()
if extras:
    failures.append(f"status not clean: {extras.splitlines()[:5]}")
subs = {}
for path, (mode, blob) in index.items():
    if mode == "160000":
        subs[path] = blob
required = ("gptp-processor", "protocol-processor", "third_party/verilog-axis")
for path in required:
    sub = clone / path
    actual = git("rev-parse", "HEAD", cwd=sub).strip()
    dirty = git("status", "--porcelain", cwd=sub).strip()
    if actual != subs.get(path) or dirty:
        failures.append(f"submodule {path}: {actual} vs {subs.get(path)} dirty={bool(dirty)}")
print(f"head {head} tree {tree}")
print(f"{checked} tracked blobs byte- and mode-checked; index == HEAD tree: {index == tracked}")
print("gitlinks: " + ", ".join(f"{p}={subs[p]}" for p in sorted(subs)))
print("INTEGRITY " + ("PASS" if not failures else "FAIL: " + "; ".join(failures)))
sys.exit(1 if failures else 0)

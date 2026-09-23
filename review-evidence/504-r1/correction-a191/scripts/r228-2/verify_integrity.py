#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned final integrity check of the review clone.

Proves, without trusting `git status`: HEAD and its tree are the reviewed
ones; every committed file's worktree bytes hash to its blob id and its mode
matches; the index equals HEAD's tree with no assume-unchanged or
skip-worktree flags; the required submodule gitlinks are pinned in the index
at stage 0 and each checkout is at the pin with its own files byte-exact.

Usage: verify_integrity.py <clone> <expected-head> <expected-tree>
"""

import os
import subprocess
import sys
from pathlib import Path

ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
REQUIRED = ("third_party/verilog-axis", "protocol-processor", "gptp-processor")


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True, env=ENV).stdout


def blob_id(path: Path) -> str:
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return subprocess.run(["git", "hash-object", "--no-filters", "--stdin"], input=data,
                          capture_output=True, check=True, env=ENV).stdout.decode().strip()


def check_tree(repo: Path, rev: str) -> tuple[int, list[str]]:
    bad, count = [], 0
    for line in git(repo, "ls-tree", "-r", "-z", "--full-tree", rev).split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        if kind == "commit":
            continue
        count += 1
        target = repo / path
        if not target.exists() and not target.is_symlink():
            bad.append(f"missing {path}")
            continue
        if mode == "120000":
            ok = target.is_symlink()
        else:
            ok = not target.is_symlink() and target.is_file()
            executable = bool(target.stat().st_mode & 0o100)
            ok = ok and executable == (mode == "100755")
        if not ok:
            bad.append(f"mode {path} {mode}")
        elif blob_id(target) != oid:
            bad.append(f"bytes {path}")
    return count, bad


def main() -> None:
    repo, head, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    out = []
    actual_head = git(repo, "rev-parse", "HEAD").strip()
    actual_tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
    out.append(f"HEAD {actual_head} expected {head}: {'OK' if actual_head == head else 'FAIL'}")
    out.append(f"tree {actual_tree} expected {tree}: {'OK' if actual_tree == tree else 'FAIL'}")
    index_tree = git(repo, "write-tree").strip()
    out.append(f"index write-tree {index_tree}: {'OK' if index_tree == tree else 'FAIL'}")
    flags = [line for line in git(repo, "ls-files", "-v").splitlines()
             if line[:1] not in ("H",)]
    out.append(f"index entries with non-H flags: {len(flags)} {flags[:5]}")
    count, bad = check_tree(repo, "HEAD")
    out.append(f"parent committed files checked: {count}; mismatches: {len(bad)} {bad[:10]}")
    for sub in REQUIRED:
        staged = [line for line in git(repo, "ls-files", "-s", "--", sub).splitlines()]
        pin = git(repo, "rev-parse", f"HEAD:{sub}").strip()
        ok_index = (len(staged) == 1 and staged[0].startswith(f"160000 {pin} 0\t"))
        sub_head = git(repo / sub, "rev-parse", "HEAD").strip()
        count, bad = check_tree(repo / sub, pin)
        out.append(f"{sub}: pin {pin} index-stage0 {'OK' if ok_index else 'FAIL'} "
                   f"checkout {sub_head} {'OK' if sub_head == pin else 'FAIL'} "
                   f"files {count} mismatches {len(bad)} {bad[:5]}")
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    out.append(f"git status --porcelain (informational): {len(status.splitlines())} line(s)")
    print("\n".join(out))


if __name__ == "__main__":
    main()

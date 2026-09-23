#!/usr/bin/env python3
"""Reviewer clone-integrity check (round R267-2, PR #533).

Proves the review clone is still the exact published head after the round's
probes: HEAD and its tree, index equal to HEAD, no hidden-index flags, every
tracked regular file's bytes (hashed with `git hash-object --no-filters`) and
mode equal to the HEAD tree, every symlink target equal, and each gitlink
either uninitialised or checked out at its pinned commit.

usage: clone_integrity.py CLONE EXPECTED_HEAD EXPECTED_TREE
"""
import os
import pathlib
import stat
import subprocess
import sys


def git(clone, *args, check=True):
    return subprocess.run(["git", "-C", str(clone), *args], capture_output=True,
                          text=True, check=check).stdout


def main() -> int:
    clone = pathlib.Path(sys.argv[1]).resolve()
    want_head, want_tree = sys.argv[2], sys.argv[3]
    problems = []
    head = git(clone, "rev-parse", "HEAD").strip()
    tree = git(clone, "rev-parse", "HEAD^{tree}").strip()
    print(f"HEAD {head}\ntree {tree}")
    if head != want_head or tree != want_tree:
        problems.append("HEAD or tree differs from the expected exact head")
    staged = git(clone, "diff-index", "--cached", "--name-only", "HEAD").split()
    print(f"index entries differing from HEAD: {len(staged)}")
    if staged:
        problems.append(f"index differs from HEAD: {staged[:10]}")
    flagged = [line for line in git(clone, "ls-files", "-v").splitlines()
               if line[:1] not in ("H",)]
    print(f"hidden-index or non-H flags: {len(flagged)}")
    problems += [f"index flag: {line}" for line in flagged]
    status = git(clone, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none")
    print(f"status entries: {len(status.splitlines())}")
    problems += [f"status: {line}" for line in status.splitlines()]
    entries = git(clone, "ls-tree", "-r", "-z", "HEAD").split("\0")
    counts = {"blob": 0, "symlink": 0, "gitlink": 0}
    for entry in filter(None, entries):
        meta, path = entry.split("\t", 1)
        mode, kind, oid = meta.split()
        full = clone / path
        if kind == "commit":
            counts["gitlink"] += 1
            sub_head = subprocess.run(["git", "-C", str(full), "rev-parse", "HEAD"],
                                      capture_output=True, text=True)
            top = subprocess.run(["git", "-C", str(full), "rev-parse", "--show-toplevel"],
                                 capture_output=True, text=True)
            initialised = sub_head.returncode == 0 and pathlib.Path(top.stdout.strip()) == full
            state = (f"checked out at {sub_head.stdout.strip()}" if initialised
                     else "not initialised")
            print(f"gitlink {path} pin {oid}: {state}")
            if initialised and sub_head.stdout.strip() != oid:
                problems.append(f"gitlink {path} off its pin")
            continue
        info = os.lstat(full)
        if mode == "120000":
            counts["symlink"] += 1
            target = os.readlink(full)
            blob = subprocess.run(["git", "-C", str(clone), "cat-file", "blob", oid],
                                  capture_output=True, check=True).stdout
            if not stat.S_ISLNK(info.st_mode) or target.encode() != blob:
                problems.append(f"symlink {path} differs")
            continue
        counts["blob"] += 1
        actual = subprocess.run(["git", "-C", str(clone), "hash-object", "--no-filters", "--", path],
                                capture_output=True, text=True, check=True).stdout.strip()
        exec_bit = bool(info.st_mode & stat.S_IXUSR)
        if not stat.S_ISREG(info.st_mode) or actual != oid or exec_bit != (mode == "100755"):
            problems.append(f"file {path} differs (mode {mode}, oid {oid}, actual {actual})")
    print(f"regular files checked: {counts['blob']}, symlinks: {counts['symlink']}, "
          f"gitlinks: {counts['gitlink']}")
    for name in ("scripts/act_ci.py", "scripts/act_slot_proof.sh",
                 "docs/testing/CI_WORKFLOWS.md", "scripts/check_baremetal_only.py"):
        oid = git(clone, "rev-parse", f"HEAD:{name}").strip()
        mode = [line.split()[0] for line in git(clone, "ls-tree", "HEAD", name).splitlines()][0]
        print(f"key {name}: mode {mode} blob {oid}")
    if problems:
        print("PROBLEMS:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("CLONE INTEGRITY: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

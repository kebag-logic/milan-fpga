#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Byte-level integrity of the reviewed clone (R227-2, issue #504 / PR #521).

For the parent and each required submodule: HEAD is the expected commit,
the index equals HEAD, no index entry carries assume-unchanged or
skip-worktree, every index entry's worktree bytes hash to its blob id with
the committed mode, and the worktree status (ignored files included) is
empty. The required gitlinks must equal their expected pins.

Usage: verify_integrity.py <clone> <expected-head> <expected-tree>
"""

import os
import subprocess
import sys
from pathlib import Path

PINS = {"third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
        "protocol-processor": "424c688fa2205b934a7689a58f2aa766420f2326",
        "gptp-processor": "c1b617435824929a790739ea8585c3fe1a328cc0"}
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(repo: Path, *args: str, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, input=data, env=ENV).stdout


def check(repo: Path, head: str, tree: str | None, problems: list, label: str) -> int:
    if git(repo, "rev-parse", "HEAD").decode().strip() != head:
        problems.append(f"{label}: HEAD is not {head}")
    if tree and git(repo, "rev-parse", "HEAD^{tree}").decode().strip() != tree:
        problems.append(f"{label}: tree is not {tree}")
    if subprocess.run(["git", "-C", str(repo), "diff-index", "--cached", "--quiet",
                       "HEAD"], env=ENV).returncode:
        problems.append(f"{label}: index differs from HEAD")
    flags = [line for line in git(repo, "ls-files", "-v").decode().splitlines()
             if line[:1].islower() or line[:1] == "S"]
    if flags:
        problems.append(f"{label}: hidden index flags {flags[:5]}")
    count = 0
    for line in git(repo, "ls-files", "-s", "-z").split(b"\0"):
        if not line:
            continue
        meta, name = line.split(b"\t", 1)
        mode, blob, stage = meta.decode().split()
        path = repo / name.decode()
        if stage != "0":
            problems.append(f"{label}: unmerged {name!r}")
            continue
        if mode == "160000":
            continue
        count += 1
        if mode == "120000":
            if not path.is_symlink():
                problems.append(f"{label}: {name!r} is not a symlink")
                continue
            content = os.readlink(path).encode()
        else:
            if path.is_symlink() or not path.is_file():
                problems.append(f"{label}: {name!r} is not a regular file")
                continue
            content = path.read_bytes()
            executable = os.access(path, os.X_OK)
            if executable != (mode == "100755"):
                problems.append(f"{label}: {name!r} mode mismatch ({mode})")
        actual = git(repo, "hash-object", "--stdin", "--no-filters", data=content)
        if actual.decode().strip() != blob:
            problems.append(f"{label}: {name!r} bytes differ from {blob}")
    status = git(repo, "status", "--porcelain", "--ignored",
                 "--untracked-files=all").decode().strip()
    if status:
        problems.append(f"{label}: status not empty: {status[:300]}")
    return count


def main() -> int:
    clone, head, tree = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    problems = []
    total = check(clone, head, tree, problems, "parent")
    print(f"parent: {total} committed files checked")
    for sub, pin in PINS.items():
        entry = git(clone, "ls-tree", "HEAD", sub).decode().split()
        if entry[:3] != ["160000", "commit", pin]:
            problems.append(f"gitlink {sub}: {entry}")
        count = check(clone / sub, pin, None, problems, sub)
        print(f"{sub}: gitlink {pin}, {count} committed files checked")
    for problem in problems:
        print("PROBLEM " + problem)
    print("INTEGRITY " + ("FAIL" if problems else "PASS"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

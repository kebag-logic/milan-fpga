#!/usr/bin/env python3
"""R500-2: prove a checkout is byte-exact at the reviewed head.

    python3 r500_2_integrity.py /path/to/checkout

Checks: HEAD and its tree; every tracked superproject file's bytes and mode
against the head's tree (blob ids recomputed from the working files); the
index equals the head's tree; the submodule gitlinks the review relies on
are the tree's, and inside each initialized one every tracked file's bytes
and mode match its HEAD; no untracked or ignored file anywhere. Exit 0 = all
hold.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HEAD = "7f8dc1b10c80c9e9631b8d6c6f5f37a039bc2e11"
TREE = "86236b61ec36ed252d6f91d698f2784302ef3743"
SUBMODULES = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          check=True).stdout


def tree_entries(repo: Path, rev: str) -> dict[str, tuple[str, str, str]]:
    out = {}
    for line in git(repo, "ls-tree", "-r", "-z", "--full-tree", rev).split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, kind, oid = meta.split()
        out[path] = (mode, kind, oid)
    return out


def blob_check(repo: Path, entries: dict[str, tuple[str, str, str]]) -> list[str]:
    """Hash every tracked file of `repo` and compare bytes and mode."""
    bad = []
    files = [p for p, (_m, k, _o) in entries.items() if k == "blob"]
    hashed = subprocess.run(["git", "-C", str(repo), "hash-object", "--no-filters", "--stdin-paths"],
                            input="\n".join(str(repo / p) if not entries[p][0] == "120000" else str(repo / p)
                                            for p in files) + "\n",
                            capture_output=True, text=True, check=True).stdout.split()
    for p, h in zip(files, hashed):
        mode, _k, oid = entries[p]
        full = repo / p
        if mode == "120000":
            target = os.readlink(full).encode()
            h = subprocess.run(["git", "hash-object", "--stdin"], input=target,
                               capture_output=True, check=True).stdout.decode().strip()
            if not full.is_symlink():
                bad.append(f"{p}: not a symlink")
        elif mode == "100755" and not os.access(full, os.X_OK):
            bad.append(f"{p}: mode 100755 expected")
        elif mode == "100644" and os.access(full, os.X_OK):
            bad.append(f"{p}: mode 100644 expected")
        if h != oid:
            bad.append(f"{p}: blob {h} != {oid}")
    return bad


def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    found = []
    head = git(repo, "rev-parse", "HEAD").strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
    if head != HEAD or tree != TREE:
        found.append(f"HEAD {head} tree {tree}")
    entries = tree_entries(repo, HEAD)
    found += blob_check(repo, entries)
    if git(repo, "write-tree").strip() != TREE:
        found.append("the index is not the head's tree")
    for sub in SUBMODULES:
        mode, kind, oid = entries[sub]
        sub_dir = repo / sub
        sub_head = git(sub_dir, "rev-parse", "HEAD").strip()
        if kind != "commit" or sub_head != oid:
            found.append(f"{sub}: gitlink {oid}, checkout {sub_head}")
            continue
        sub_entries = tree_entries(sub_dir, "HEAD")
        sb = blob_check(sub_dir, sub_entries)
        found += [f"{sub}/{x}" for x in sb]
        if git(sub_dir, "status", "--porcelain", "--ignored").strip():
            found.append(f"{sub}: untracked, ignored or modified files")
        print(f"submodule {sub}: pin {oid}, {sum(1 for e in sub_entries.values() if e[1] == 'blob')} "
              f"blobs, {len(sb)} mismatches")
    status = git(repo, "status", "--porcelain", "--ignored", "--ignore-submodules=none")
    if status.strip():
        found.append("superproject status not empty:\n" + status)
    n = sum(1 for e in entries.values() if e[1] == "blob")
    print(f"superproject: HEAD {head} tree {tree}, {n} blobs checked")
    for x in found:
        print(f"FINDING: {x}")
    print("integrity: OK" if not found else f"integrity: {len(found)} finding(s)")
    return 0 if not found else 1


if __name__ == "__main__":
    sys.exit(main())

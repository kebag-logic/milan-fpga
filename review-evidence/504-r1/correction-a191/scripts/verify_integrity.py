#!/usr/bin/env python3
"""Final integrity of the lane checkout at its committed head (A191, #504).

Usage: verify_integrity.py <checkout> <expected-head> <submodule>...

Checks, each printed with its result:
  - HEAD and its tree are the expected ones;
  - the index equals HEAD and no index entry is flagged assume-unchanged or
    skip-worktree (`git ls-files -v` prints `h`/`S` for those);
  - every tracked regular file and symlink hashes to the blob and mode HEAD
    records, read from disk (so an index told to stay quiet cannot hide one);
  - `git status --porcelain` is empty, and the ignored entries are listed;
  - each named submodule is checked out at the gitlink HEAD records, with a
    clean status of its own.
Exit 0 only when all hold.
"""
import os
import stat
import subprocess
import sys
from pathlib import Path


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    root, expected = Path(sys.argv[1]).resolve(), sys.argv[2]
    subs = sys.argv[3:]
    faults = []
    head = git(root, "rev-parse", "HEAD").strip()
    tree = git(root, "rev-parse", "HEAD^{tree}").strip()
    print(f"HEAD {head}\nTREE {tree}")
    if head != expected:
        faults.append(f"HEAD is {head}, expected {expected}")
    if subprocess.run(["git", "-C", str(root), "diff", "--cached", "--quiet"]).returncode:
        faults.append("index differs from HEAD")
    flagged = [line for line in git(root, "ls-files", "-v").splitlines()
               if line[:1] in ("h", "S", "s")]
    print(f"index flags assume-unchanged/skip-worktree: {len(flagged)}")
    faults += [f"flagged index entry: {line}" for line in flagged]
    checked = 0
    for line in git(root, "ls-tree", "-r", "-z", "--full-tree", "HEAD").split("\0"):
        if not line:
            continue
        meta, path = line.split("\t", 1)
        mode, kind, blob = meta.split()
        if kind != "blob":
            continue
        disk = root / path
        if mode == "120000":
            if not disk.is_symlink():
                faults.append(f"{path}: not a symlink on disk")
                continue
            data = os.readlink(disk).encode()
        else:
            if disk.is_symlink() or not disk.is_file():
                faults.append(f"{path}: not a regular file on disk")
                continue
            data = disk.read_bytes()
            executable = bool(disk.stat().st_mode & stat.S_IXUSR)
            if executable != (mode == "100755"):
                faults.append(f"{path}: mode {mode} but executable={executable}")
        got = subprocess.run(["git", "hash-object", "--stdin"], input=data,
                             capture_output=True, check=True).stdout.decode().strip()
        if got != blob:
            faults.append(f"{path}: disk blob {got} != HEAD {blob}")
        checked += 1
    print(f"tracked blobs byte/mode checked: {checked}")
    status = git(root, "status", "--porcelain")
    print(f"status --porcelain entries: {len(status.splitlines())}")
    if status.strip():
        faults.append("status not clean:\n" + status)
    ignored = [line for line in git(root, "status", "--porcelain", "--ignored").splitlines()
               if line.startswith("!!")]
    print(f"ignored entries: {len(ignored)} {ignored}")
    for sub in subs:
        pin = git(root, "ls-tree", "HEAD", sub).split()[2]
        at = git(root / sub, "rev-parse", "HEAD").strip()
        dirty = git(root / sub, "status", "--porcelain")
        print(f"submodule {sub}: gitlink {pin} checkout {at} clean={not dirty.strip()}")
        if pin != at:
            faults.append(f"{sub}: checkout {at} != gitlink {pin}")
        if dirty.strip():
            faults.append(f"{sub}: dirty")
    print("INTEGRITY " + ("PASS" if not faults else "FAIL:\n" + "\n".join(faults)))
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())

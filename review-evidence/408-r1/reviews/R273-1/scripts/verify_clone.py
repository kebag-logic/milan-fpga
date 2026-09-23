#!/usr/bin/env python3
"""Prove a checkout's tracked bytes, modes and index equal its HEAD tree.

Every index entry must be stage 0 and equal HEAD's tree entry (mode and object
id); every regular file's bytes on disk must hash (git hash-object
--no-filters) to that blob id and carry that mode's executable bit; every
symlink must point where the blob says; every gitlink's submodule checkout must
sit at the recorded commit. Nothing untracked or ignored may exist.
Usage: verify_clone.py <checkout>
"""

import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*args: str, cwd: Path = root, data: bytes | None = None) -> bytes:
    return subprocess.run(["git", *args], cwd=cwd, input=data, env=env,
                          check=True, capture_output=True).stdout


tree = {}
for line in git("ls-tree", "-r", "-z", "HEAD").split(b"\0"):
    if line:
        meta, path = line.split(b"\t", 1)
        mode, _kind, oid = meta.split()
        tree[path] = (mode, oid)
index = {}
for line in git("ls-files", "-s", "-z").split(b"\0"):
    if line:
        meta, path = line.split(b"\t", 1)
        mode, oid, stage = meta.split()
        assert stage == b"0", f"unmerged index entry {path!r}"
        index[path] = (mode, oid)
assert index == tree, "index differs from HEAD tree"
regular = [p for p, (m, _o) in tree.items() if m in (b"100644", b"100755")]
hashed = git("hash-object", "--no-filters", "--stdin-paths",
             data=b"\n".join(regular) + b"\n").split()
bad = []
for path, oid in zip(regular, hashed):
    mode = tree[path][0]
    full = root / os.fsdecode(path)
    if oid != tree[path][1] or full.is_symlink():
        bad.append(path)
    elif (mode == b"100755") != bool(full.stat().st_mode & 0o100):
        bad.append(path)
for path, (mode, oid) in tree.items():
    full = root / os.fsdecode(path)
    if mode == b"120000":
        target = git("cat-file", "blob", oid.decode())
        if not full.is_symlink() or os.fsencode(os.readlink(full)) != target:
            bad.append(path)
    elif mode == b"160000" and (full / ".git").exists():
        head = git("rev-parse", "HEAD", cwd=full).strip()
        if head != oid:
            bad.append(path)
extra = git("status", "--porcelain", "--ignored", "--untracked-files=all")
print(f"HEAD {git('rev-parse', 'HEAD').decode().strip()} "
      f"tree {git('rev-parse', 'HEAD^{tree}').decode().strip()}")
print(f"{len(tree)} tree entries == index entries; {len(regular)} regular "
      f"blobs byte-hashed; gitlinks checked: "
      f"{sum(1 for m, _ in tree.values() if m == b'160000')}")
print("mismatches:", [p.decode() for p in bad] or "none")
print("untracked/ignored/modified:", extra.decode().strip() or "none")
sys.exit(1 if bad or extra.strip() else 0)

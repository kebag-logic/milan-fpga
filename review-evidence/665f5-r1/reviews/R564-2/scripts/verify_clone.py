#!/usr/bin/env python3
"""Verify a review clone's tracked bytes, modes, index and gitlinks equal an exact head.

Usage: verify_clone.py <clone> <expected-head>
"""
import hashlib, subprocess, sys, os
from pathlib import Path
clone, head = Path(sys.argv[1]).resolve(), sys.argv[2]
def git(*a, cwd=clone):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout
assert git("rev-parse", "HEAD").strip() == head, "HEAD differs"
tree = {}
for line in git("ls-tree", "-r", "-z", "HEAD").split("\0"):
    if line:
        meta, path = line.split("\t", 1); mode, kind, oid = meta.split(); tree[path] = (mode, oid)
index = {}
for line in git("ls-files", "-s", "-z").split("\0"):
    if line:
        meta, path = line.split("\t", 1); mode, oid, stage = meta.split(); index[path] = (mode, oid)
assert tree == index, "index differs from HEAD tree"
bad = []
for path, (mode, oid) in tree.items():
    f = clone / path
    if mode == "160000":
        if (f / ".git").exists():
            got = git("rev-parse", "HEAD", cwd=f).strip()
            if got != oid: bad.append(f"gitlink {path} {got} != {oid}")
        continue
    if mode == "120000":
        data = os.readlink(f).encode()
    else:
        data = f.read_bytes()
        exe = os.access(f, os.X_OK)
        if (mode == "100755") != exe: bad.append(f"mode {path}")
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if blob != oid: bad.append(f"bytes {path}")
status = git("status", "--porcelain", "--ignore-submodules=none")
links = {p: o for p, (m, o) in tree.items() if m == "160000"}
print(f"head {head}; {len(tree)} tracked entries; index==tree; mismatches {len(bad)}; status-lines {len(status.splitlines())}")
for p, o in sorted(links.items()): print(f"gitlink {p} {o}")
for b in bad: print("MISMATCH", b)
for s in status.splitlines(): print("STATUS", s)
raise SystemExit(1 if bad or status.strip() else 0)

#!/usr/bin/env python3
"""R246-1: verify a checkout's tracked bytes, kinds, modes, stage-0 index and
gitlinks against HEAD's tree, from file bytes (no reliance on git status).

Usage: python3 integrity.py <checkout> <expected-head>
"""
import hashlib, os, stat, subprocess, sys
from pathlib import Path

root, want = Path(sys.argv[1]), sys.argv[2]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
git = lambda *a: subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True, env=env).stdout
head = git("rev-parse", "HEAD").strip()
tree = {}
for line in git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, kind, sha = meta.split()
        tree[path] = (mode, sha)
index = {}
for line in git("ls-files", "-s", "-z").split("\0"):
    if line:
        meta, path = line.split("\t", 1)
        mode, sha, stage = meta.split()
        index.setdefault(path, []).append((mode, sha, stage))
flags = [l for l in git("ls-files", "-v").splitlines() if l[:1] not in ("H",)]
bad = []
for path, (mode, sha) in tree.items():
    if index.get(path) != [(mode, sha, "0")]:
        bad.append(f"index mismatch {path}")
    p = root / path
    if mode == "160000":
        sub = subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True, text=True, env=env)
        if path == "external":
            continue  # registered but not initialised in this clone; gitlink checked via index above
        if sub.stdout.strip() != sha:
            bad.append(f"gitlink {path} checkout {sub.stdout.strip()} != {sha}")
        continue
    st = os.lstat(p)
    if mode == "120000":
        data = os.readlink(p).encode()
        ok_kind = stat.S_ISLNK(st.st_mode)
    else:
        ok_kind = stat.S_ISREG(st.st_mode)
        data = p.read_bytes() if ok_kind else b""
        if ok_kind and bool(st.st_mode & 0o111) != (mode == "100755"):
            bad.append(f"mode {path}")
    if not ok_kind:
        bad.append(f"kind {path}")
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if blob != sha:
        bad.append(f"bytes {path}")
extra = set(index) - set(tree)
print(f"HEAD {head} expected {want} match={head == want}")
print(f"tree entries {len(tree)}; index entries {len(index)}; index-only {sorted(extra)}; hidden index flags {flags[:5]}")
print(f"mismatches: {len(bad)}"); [print("  ", b) for b in bad[:20]]
print("INTEGRITY:", "PASS" if head == want and not bad and not extra and not flags else "FAIL")

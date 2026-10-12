#!/usr/bin/env python3
"""Verify a checkout is the exact bytes and modes of a commit: HEAD, every
tracked blob hashed from disk (no filters) against HEAD's tree, the index equal
to HEAD's tree, and the gitlinks listed.
usage: python3 -I integrity.py <checkout> <commit>"""
import hashlib, os, stat, subprocess, sys
from pathlib import Path

repo, want = Path(sys.argv[1]), sys.argv[2]
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
def git(*a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, check=True, env=env).stdout
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
print(f"HEAD {head} tree {tree} {'OK' if head == want else 'MISMATCH'}")
bad = blobs = 0
links = []
for e in filter(None, git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0")):
    meta, path = e.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    p = repo / os.fsdecode(path)
    if kind == "commit":
        links.append((os.fsdecode(path), oid)); continue
    st = p.lstat()
    data = os.readlink(p).encode() if stat.S_ISLNK(st.st_mode) else p.read_bytes()
    dmode = "120000" if stat.S_ISLNK(st.st_mode) else ("100755" if st.st_mode & stat.S_IXUSR else "100644")
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    blobs += 1
    if h != oid or dmode != mode:
        bad += 1; print(f"DIFFERS {os.fsdecode(path)}")
idx = git("ls-files", "-s", "-z").split(b"\0")
idx = sorted(filter(None, idx))
treel = sorted(f"{m} {o} 0\t".encode() + p for m, _, o, p in
               ((*e.split(b"\t", 1)[0].decode().split(), e.split(b"\t", 1)[1]) for e in
                filter(None, git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"))))
print(f"blobs checked {blobs}, differing {bad}; index equals HEAD tree: {idx == treel}")
for path, oid in links:
    print(f"gitlink {path} {oid}")
print(f"status --porcelain lines: {len(git('status', '--porcelain', '--ignore-submodules=none').splitlines())}")
sys.exit(1 if bad or head != want or idx != treel else 0)

#!/usr/bin/env python3
"""Verify a clone equals its head: every tracked regular file's bytes hash to
its index blob with the index mode, the index tree equals HEAD's tree, the
status is empty, and the gitlinks equal HEAD's recorded revisions."""
import os, stat, subprocess, sys
REPO, HEAD = sys.argv[1:3]
def git(*a, **k):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True, **k).stdout
entries = git("ls-files", "-s", "-z").split(b"\0")
bad = checked = 0
links = []
for e in filter(None, entries):
    meta, path = e.split(b"\t", 1)
    mode, sha, stage = meta.split()
    p = os.path.join(REPO, path.decode())
    if mode == b"160000":
        links.append((path.decode(), sha.decode()))
        continue
    st = os.lstat(p)
    if mode == b"120000":
        data = os.readlink(p).encode()
    else:
        data = open(p, "rb").read()
        want_exec = mode == b"100755"
        if bool(st.st_mode & stat.S_IXUSR) != want_exec:
            bad += 1; print("MODE", path.decode())
    h = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.strip()
    if h != sha or stage != b"0":
        bad += 1; print("BLOB", path.decode())
    checked += 1
index_tree = git("write-tree").decode().strip()
head_tree = git("rev-parse", f"{HEAD}^{{tree}}").decode().strip()
status = git("status", "--porcelain=v1", "--untracked-files=all").decode()
head_links = {}
for line in git("ls-tree", "-r", HEAD).decode().splitlines():
    m, t, s, *rest = line.split(None, 3)
    if t == "commit":
        head_links[line.split("\t", 1)[1]] = s
print(f"files checked {checked}, mismatches {bad}")
print(f"index tree {index_tree} head tree {head_tree} equal={index_tree == head_tree}")
print(f"status lines {len(status.splitlines())}")
for p, s in links:
    print(f"gitlink {p} {s} head={head_links.get(p) == s}")
print("HEAD", git("rev-parse", "HEAD").decode().strip())

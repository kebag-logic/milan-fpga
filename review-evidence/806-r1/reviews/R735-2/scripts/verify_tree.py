#!/usr/bin/env python3
"""Verify a checkout equals a commit: every tracked blob's bytes and mode, stage-0 index entries without
hidden flags, gitlinks, and a clean status. usage: verify_tree.py <repo> <commit>"""
import os, stat, subprocess, sys
repo, commit = sys.argv[1], sys.argv[2]
g = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout
head = g("rev-parse", "HEAD").decode().strip()
tree = {}
for rec in g("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1); mode, typ, oid = meta.decode().split(); tree[path.decode()] = (mode, oid)
idx = {}
for rec in g("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1); mode, oid, st = meta.decode().split(); idx[path.decode()] = (mode, oid, st)
flags = [l for l in g("ls-files", "-v").decode().splitlines() if not l.startswith("H ")]
bad = []
for p, (mode, oid) in tree.items():
    if p not in idx or idx[p][:2] != (mode, oid) or idx[p][2] != "0": bad.append(("index", p)); continue
    f = os.path.join(repo, p)
    if mode == "160000": continue
    if mode == "120000":
        if not os.path.islink(f) or os.readlink(f).encode() != g("cat-file", "blob", oid): bad.append(("link", p))
        continue
    with open(f, "rb") as fh: data = fh.read()
    if subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True).stdout.decode().strip() != oid:
        bad.append(("bytes", p))
    if bool(os.stat(f).st_mode & stat.S_IXUSR) != (mode == "100755"): bad.append(("mode", p))
extra = set(idx) - set(tree)
links = {p: oid for p, (m, oid) in tree.items() if m == "160000"}
sub = g("submodule", "status").decode()
status = g("status", "--porcelain", "--ignore-submodules=none").decode()
print("HEAD", head, "== commit", head == g("rev-parse", commit).decode().strip())
print("tracked", len(tree), "bad", bad[:10], "extra index", sorted(extra)[:5], "hidden flags", flags[:5])
for p, oid in sorted(links.items()):
    print("gitlink", p, oid)
print("submodule status:\n" + sub, "status porcelain:", repr(status))
sys.exit(0 if (head == g("rev-parse", commit).decode().strip() and not bad and not extra and not flags and not status) else 1)

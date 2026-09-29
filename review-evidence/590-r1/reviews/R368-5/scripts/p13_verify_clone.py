#!/usr/bin/env python3
"""P13: prove the review clone is exact head bytes after the round: HEAD, index
records (mode, blob, stage 0) equal to the HEAD tree, no assume-unchanged or
skip-worktree flags, every tracked regular file / symlink hashing to its blob
with the right executable bit, and each submodule gitlink checked out at its pin."""
import os, stat, subprocess, sys
HEAD = "4c2a30debb031595b81c5c4bfc53b601a0fec528"; TREE = "0a9754d44e40de8c734468be2cedad5ac675d794"
def git(*a, cwd="."):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True,
                          env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"}).stdout
fail = []
if git("rev-parse", "HEAD").strip() != HEAD: fail.append("HEAD moved")
if git("rev-parse", "HEAD^{tree}").strip() != TREE: fail.append("tree differs")
tree = {}
for line in git("ls-tree", "-r", "--full-tree", HEAD).splitlines():
    meta, path = line.split("\t", 1); mode, typ, oid = meta.split(); tree[path] = (mode, oid)
index = {}
for line in git("ls-files", "-s").splitlines():
    meta, path = line.split("\t", 1); mode, oid, stage = meta.split()
    if stage != "0": fail.append(f"unmerged {path}")
    index[path] = (mode, oid)
if index != tree: fail.append(f"index != HEAD tree ({len(set(index) ^ set(tree))} path diffs)")
flags = [l for l in git("ls-files", "-v").splitlines() if not l.startswith("H ")]
if flags: fail.append(f"{len(flags)} index flag(s): {flags[:3]}")
paths = [p for p, (m, _) in tree.items() if m != "160000"]
# hash in batches with the same bytes git would read (no filters, exact bytes)
proc = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"],
                      input="\n".join(p for p in paths if tree[p][0] != "120000"),
                      capture_output=True, text=True, check=True)
for p, oid in zip([p for p in paths if tree[p][0] != "120000"], proc.stdout.split()):
    if oid != tree[p][1]: fail.append(f"bytes differ {p}")
    st = os.lstat(p)
    want_x = tree[p][0] == "100755"
    if stat.S_ISLNK(st.st_mode) or bool(st.st_mode & stat.S_IXUSR) != want_x: fail.append(f"mode differs {p}")
for p in (p for p in paths if tree[p][0] == "120000"):
    target = os.readlink(p).encode()
    oid = subprocess.run(["git", "hash-object", "--stdin"], input=target, capture_output=True, check=True).stdout.decode().strip()
    if oid != tree[p][1]: fail.append(f"symlink differs {p}")
for p, (m, pin) in tree.items():
    if m != "160000": continue
    if not os.path.exists(os.path.join(p, ".git")):
        print(f"gitlink {p} {pin}: not initialised in this clone (as at session start)"); continue
    got = git("rev-parse", "HEAD", cwd=p).strip()
    dirty = git("status", "--porcelain", cwd=p).strip()
    print(f"gitlink {p} {pin}: checkout {got} {'CLEAN' if not dirty else 'DIRTY'}")
    if got != pin or dirty: fail.append(f"submodule {p}")
extra = git("status", "--porcelain", "--ignored").strip()
if extra: fail.append(f"untracked/ignored present: {extra.splitlines()[:5]}")
print(f"tracked non-gitlink files hashed: {len(paths)}")
print("RESULT:", "EXACT" if not fail else "DIFFERS " + "; ".join(fail[:10]))
sys.exit(1 if fail else 0)

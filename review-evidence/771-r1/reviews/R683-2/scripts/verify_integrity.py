#!/usr/bin/env python3
"""Verify a checkout is byte-exact at HEAD: index == HEAD tree, every tracked
blob's bytes and mode in the worktree, and each submodule's HEAD == its
gitlink with a clean status. usage: verify_integrity.py <repo> [required sub=sha ...]"""
import os, stat, subprocess, sys
repo = sys.argv[1]
def git(*a, cwd=repo):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True).stdout
bad = 0
tree = {}
for rec in git("ls-tree", "-r", "-z", "HEAD").split(b"\0"):
    if not rec: continue
    meta, path = rec.split(b"\t", 1); mode, typ, sha = meta.split()
    tree[path.decode()] = (mode.decode(), sha.decode())
index = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if not rec: continue
    meta, path = rec.split(b"\t", 1); mode, sha, st = meta.split()
    if st != b"0": print("UNMERGED", path); bad += 1
    index[path.decode()] = (mode.decode(), sha.decode())
if index != tree:
    print("INDEX != HEAD", len(set(index.items()) ^ set(tree.items()))); bad += 1
files = [p for p, (m, _) in tree.items() if m in ("100644", "100755")]
out = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], cwd=repo, input="\n".join(files).encode(),
                     check=True, capture_output=True).stdout.decode().split()
for p, h in zip(files, out):
    m, sha = tree[p]
    if h != sha: print("BYTES", p); bad += 1
    x = bool(os.stat(os.path.join(repo, p)).st_mode & stat.S_IXUSR)
    if x != (m == "100755"): print("MODE", p); bad += 1
for p, (m, sha) in tree.items():
    if m == "120000":
        if os.readlink(os.path.join(repo, p)).encode() != git("cat-file", "blob", sha): print("SYMLINK", p); bad += 1
subs = {p: sha for p, (m, sha) in tree.items() if m == "160000"}
for p, sha in sorted(subs.items()):
    d = os.path.join(repo, p)
    if not os.path.exists(os.path.join(d, ".git")):
        print(f"submodule {p}: not initialized (gitlink {sha})"); continue
    h = git("rev-parse", "HEAD", cwd=d).decode().strip()
    dirty = git("status", "--porcelain", cwd=d).decode().strip()
    ok = h == sha and not dirty
    print(f"submodule {p}: head {h} gitlink {sha} {'clean' if not dirty else 'DIRTY'} {'OK' if ok else 'FAIL'}")
    bad += not ok
for req in sys.argv[2:]:
    p, sha = req.split("=")
    if subs.get(p) != sha: print("REQUIRED-GITLINK", p, subs.get(p), "!=", sha); bad += 1
st = git("status", "--porcelain", "--ignore-submodules=none").decode().strip()
if st: print("STATUS not clean:\n" + st); bad += 1
print(f"HEAD {git('rev-parse','HEAD').decode().strip()} tree {git('rev-parse','HEAD^{tree}').decode().strip()}: "
      f"{len(files)} blobs checked, {len(subs)} gitlinks, failures {bad}")
sys.exit(1 if bad else 0)

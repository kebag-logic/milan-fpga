#!/usr/bin/env python3
"""Prove a checkout equals its HEAD: every HEAD tree entry has the same mode and
blob id in the index (stage 0) and the same bytes and mode on disk; gitlinks are
stage-0 records at the HEAD commit, and initialised submodules sit at that
commit with clean trees. Usage: verify_tree.py <checkout>"""
import os, stat, subprocess, sys

root = sys.argv[1]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*a, cwd=root, inp=None):
    return subprocess.run(["git", *a], cwd=cwd, env=env, input=inp,
                          capture_output=True, check=True).stdout


tree = {}
for rec in git("ls-tree", "-r", "-z", "--full-tree", "HEAD").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, _, sha = meta.split()
        tree[path.decode()] = (mode.decode(), sha.decode())
index = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, sha, st = meta.split()
        index.setdefault(path.decode(), []).append((mode.decode(), sha.decode(), st.decode()))
bad = []
if set(tree) != set(index):
    bad.append(f"path sets differ: {sorted(set(tree) ^ set(index))[:10]}")
blobs = [p for p, (m, _) in tree.items() if m != "160000"]
for p, (m, s) in tree.items():
    ent = index.get(p, [])
    if ent != [(m, s, "0")]:
        bad.append(f"index {p}: {ent} != {(m, s, '0')}")
hashes = git("hash-object", "--no-filters", "--stdin-paths", inp="\n".join(blobs).encode()).decode().split()
for p, h in zip(blobs, hashes):
    m, s = tree[p]
    full = os.path.join(root, p)
    st_ = os.lstat(full)
    if m == "120000":
        ok_mode = stat.S_ISLNK(st_.st_mode)
    else:
        ok_mode = stat.S_ISREG(st_.st_mode) and (bool(st_.st_mode & 0o100) == (m == "100755"))
    if m == "120000":
        h = git("hash-object", "--stdin", inp=os.readlink(full).encode()).decode().strip()
    if h != s or not ok_mode:
        bad.append(f"worktree {p}: {h} mode_ok={ok_mode}")
links = {p: s for p, (m, s) in tree.items() if m == "160000"}
for p, s in sorted(links.items()):
    sub = os.path.join(root, p)
    if os.path.exists(os.path.join(sub, ".git")):
        head = git("rev-parse", "HEAD", cwd=sub).decode().strip()
        dirty = git("status", "--porcelain", "--untracked-files=all", "--ignored", cwd=sub).decode()
        state = f"initialised head={head} clean={not dirty}"
        if head != s or dirty:
            bad.append(f"submodule {p}: {state}")
    else:
        state = "not initialised"
    print(f"gitlink {p} {s} stage0 {state}")
extra = git("status", "--porcelain", "--untracked-files=all", "--ignored").decode()
if extra:
    bad.append("status not empty: " + extra[:400])
print(f"HEAD {git('rev-parse', 'HEAD').decode().strip()} tree {git('rev-parse', 'HEAD^{tree}').decode().strip()}")
print(f"tree entries {len(tree)}, blobs hashed {len(blobs)}, gitlinks {len(links)}")
print("RESULT:", "PASS" if not bad else "FAIL")
for b in bad[:50]:
    print(" ", b)
sys.exit(1 if bad else 0)

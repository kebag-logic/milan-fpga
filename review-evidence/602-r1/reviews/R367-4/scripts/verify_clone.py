#!/usr/bin/env python3
"""Prove a checkout carries its HEAD bytes: index == HEAD tree, every tracked
blob's bytes and mode match its index entry (content re-hashed, no stat
cache), no untracked/ignored residue, and each gitlink equals the
submodule's checked-out HEAD (whose own blobs are verified the same way).
Usage: verify_clone.py <repo> <expected-head>"""
import os
import stat
import subprocess
import sys


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", repo, *args], check=True, input=data,
                          capture_output=True).stdout


def verify(repo, label):
    bad = 0
    head_tree = git(repo, "rev-parse", "HEAD^{tree}").decode().strip()
    index_tree = git(repo, "write-tree").decode().strip()
    print(f"{label}: HEAD tree {head_tree}; index tree {index_tree}")
    bad += head_tree != index_tree
    entries = git(repo, "ls-files", "-s", "-z").decode().split("\0")
    blobs = links = 0
    paths, want = [], []
    for e in entries:
        if not e:
            continue
        meta, path = e.split("\t", 1)
        mode, oid, stage = meta.split()
        bad += stage != "0"
        full = os.path.join(repo, path)
        if mode == "160000":
            if not os.path.exists(os.path.join(full, ".git")):
                empty = not os.listdir(full) if os.path.isdir(full) else False
                print(f"{label}: gitlink {path} {oid} not initialised "
                      f"({'empty directory' if empty else 'NOT EMPTY'})")
                bad += not empty
                continue
            sub = git(full, "rev-parse", "HEAD").decode().strip()
            links += 1
            print(f"{label}: gitlink {path} {oid} checkout {sub} {'OK' if sub == oid else 'MISMATCH'}")
            bad += sub != oid
            continue
        st = os.lstat(full)
        if mode == "120000":
            ok = stat.S_ISLNK(st.st_mode)
        else:
            ok = stat.S_ISREG(st.st_mode) and (
                bool(st.st_mode & 0o100) == (mode == "100755"))
        if not ok:
            print(f"{label}: MODE {path} {mode} {oct(st.st_mode)}")
            bad += 1
        paths.append(path)
        want.append(oid)
        blobs += 1
    got = git(repo, "hash-object", "--no-filters", "--stdin-paths",
              data="\n".join(paths).encode()).decode().split()
    for p, w, g in zip(paths, want, got):
        if w != g:
            # symlinks hash their target text
            if os.path.islink(os.path.join(repo, p)):
                g2 = git(repo, "hash-object", "--stdin",
                         data=os.readlink(os.path.join(repo, p)).encode()).decode().strip()
                if g2 == w:
                    continue
            print(f"{label}: BYTES {p} want {w} got {g}")
            bad += 1
    residue = git(repo, "status", "--porcelain", "--ignored", "--untracked-files=all").decode()
    if residue.strip():
        print(f"{label}: RESIDUE\n{residue}")
        bad += 1
    print(f"{label}: {blobs} blobs re-hashed, {links} gitlinks, {bad} problem(s)")
    return bad


repo, expect = sys.argv[1], sys.argv[2]
head = git(repo, "rev-parse", "HEAD").decode().strip()
print(f"HEAD {head} expected {expect} {'OK' if head == expect else 'MISMATCH'}")
problems = int(head != expect) + verify(repo, "super")
for line in git(repo, "submodule", "status").decode().splitlines():
    flag, sha, path = line[0], line[1:41], line[42:].split(" (")[0]
    if flag == "-":
        print(f"submodule {path}: not initialised ({sha}); not a build input here")
        continue
    problems += verify(os.path.join(repo, path), path)
print("VERIFY:", "PASS" if problems == 0 else f"FAIL ({problems})")
sys.exit(1 if problems else 0)

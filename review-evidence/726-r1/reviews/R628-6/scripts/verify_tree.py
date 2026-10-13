#!/usr/bin/env python3
"""Verify a review clone against its exact head without writing to it.

Usage: verify_tree.py CLONE HEAD_SHA TREE_SHA
Checks: HEAD and tree identity; every tracked regular file's working bytes
hash to its HEAD blob and its mode matches; the stage-0 index equals the HEAD
tree (no other stages, no assume-unchanged/skip-worktree flags); the status
(including ignored files) is empty; each gitlink equals the base commit's and,
for initialized submodules, the submodule checkout is at that commit and clean.
Prints one line per check and exits non-zero on any mismatch.
"""
import os
import stat
import subprocess
import sys

os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True).stdout


clone, head, tree = sys.argv[1:4]
bad = 0


def report(ok, what):
    global bad
    bad += not ok
    print(("OK   " if ok else "FAIL ") + what)


report(git("rev-parse", "HEAD", cwd=clone).decode().strip() == head, f"HEAD == {head}")
report(git("rev-parse", "HEAD^{tree}", cwd=clone).decode().strip() == tree, f"tree == {tree}")
entries = git("ls-tree", "-r", "-z", "HEAD", cwd=clone).split(b"\0")
blobs, links = [], []
for e in entries:
    if not e:
        continue
    meta, path = e.split(b"\t", 1)
    mode, typ, sha = meta.split()
    (links if typ == b"commit" else blobs).append((mode.decode(), sha.decode(), path.decode()))
paths = [p for m, s, p in blobs if m != "120000"]
proc = subprocess.run(["git", "hash-object", "--no-filters", "--stdin-paths"], cwd=clone,
                      input="\n".join(paths).encode(), capture_output=True, check=True)
got = proc.stdout.decode().split()
want = [s for m, s, p in blobs if m != "120000"]
mism = [p for p, g, w in zip(paths, got, want) if g != w]
report(len(got) == len(want) and not mism, f"{len(paths)} regular-file blobs byte-identical" + (f" (mismatch: {mism[:5]})" if mism else ""))
mode_bad = []
for m, s, p in blobs:
    st = os.lstat(os.path.join(clone, p))
    if m == "120000":
        if not stat.S_ISLNK(st.st_mode):
            mode_bad.append(p)
        else:
            raw = os.readlink(os.path.join(clone, p)).encode()
            digest = subprocess.run(["git", "hash-object", "--stdin"], input=raw,
                                    cwd=clone, capture_output=True, check=True).stdout.decode().strip()
            if digest != s:
                mode_bad.append(p)
    else:
        exe = bool(st.st_mode & 0o111)
        if not stat.S_ISREG(st.st_mode) or (m == "100755") != exe:
            mode_bad.append(p)
report(not mode_bad, f"{len(blobs)} tracked modes match" + (f" (bad: {mode_bad[:5]})" if mode_bad else ""))
idx = git("ls-files", "-s", "-v", "-z", cwd=clone).split(b"\0")
idx_entries, flags_bad, stage_bad = {}, [], []
for e in idx:
    if not e:
        continue
    meta, path = e.split(b"\t", 1)
    tag, mode, sha, stage = meta.split()
    if tag != b"H":
        flags_bad.append(path.decode())
    if stage != b"0":
        stage_bad.append(path.decode())
    idx_entries[path.decode()] = (mode.decode(), sha.decode())
tree_entries = {p: (m, s) for m, s, p in blobs + links}
report(idx_entries == tree_entries and not flags_bad and not stage_bad,
       f"index == HEAD tree ({len(idx_entries)} entries; flags {len(flags_bad)}, non-zero stages {len(stage_bad)})")
st = git("status", "--porcelain=v1", "--ignored", "--untracked-files=all", cwd=clone).decode()
report(st.strip() == "", "status (incl. ignored, untracked) empty" + ("" if not st.strip() else f": {st[:200]}"))
base_links = []
for e in git("ls-tree", "-r", "-z", "c6bd08c6", cwd=clone).split(b"\0"):
    if e.startswith(b"160000 commit "):
        meta, path = e.split(b"\t", 1)
        mode, typ, sha = meta.split()
        base_links.append((mode.decode(), sha.decode(), path.decode()))
report(links == base_links, f"all {len(links)} gitlinks equal source base c6bd08c6")
for m, s, p in links:
    sub = os.path.join(clone, p)
    if os.path.exists(os.path.join(sub, ".git")):
        cur = git("rev-parse", "HEAD", cwd=sub).decode().strip()
        dirty = git("status", "--porcelain", cwd=sub).decode().strip()
        report(cur == s and not dirty, f"submodule {p} at gitlink {s[:12]}, clean")
    else:
        report(True, f"submodule {p} uninitialized; gitlink {s[:12]}")
sys.exit(1 if bad else 0)

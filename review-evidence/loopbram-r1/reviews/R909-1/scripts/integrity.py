#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove a checkout equals its HEAD: every tracked blob's on-disk bytes and
mode, the index (mode, id, stage 0, no assume-unchanged/skip-worktree flag),
each gitlink against the submodule's checked-out commit, a clean status, and
HEAD/tree ids. Usage: integrity.py <checkout> <expected head> <expected tree>"""
import os
import stat
import subprocess
import sys

repo, want_head, want_tree = sys.argv[1:4]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(*a, cwd=repo):
    return subprocess.check_output(["git", "-C", cwd, *a], env=env)


bad = []
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
if head != want_head or tree != want_tree:
    bad.append(f"head/tree {head}/{tree}")
entries = {}
for rec in git("ls-tree", "-r", "-z", "HEAD").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        entries[path.decode()] = (mode, kind, oid)
index = {}
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if rec:
        meta, path = rec.split(b"\t", 1)
        mode, oid, stage = meta.decode().split()
        index[path.decode()] = (mode, oid, stage)
if set(index) != set(entries):
    bad.append(f"index paths differ: {len(set(index) ^ set(entries))}")
for path, (mode, kind, oid) in entries.items():
    im = index.get(path)
    if im != (mode, oid, "0"):
        bad.append(f"index {path}: {im}")
flags = [l for l in git("ls-files", "-v").decode().splitlines() if not l.startswith("H ")]
if flags:
    bad.append(f"index flags: {flags[:5]}")
blobs = [p for p, (m, k, o) in entries.items() if k == "blob"]
# hash in batches, without filters, so on-disk bytes are what is proved
out = subprocess.run(["git", "-C", repo, "hash-object", "--no-filters", "--stdin-paths"],
                     input="\n".join(p for p in blobs if entries[p][0] != "120000").encode(),
                     capture_output=True, env=env, check=True).stdout.decode().split()
regular = [p for p in blobs if entries[p][0] != "120000"]
for path, got in zip(regular, out):
    mode, _, oid = entries[path]
    st = os.lstat(os.path.join(repo, path))
    want_exec = mode == "100755"
    if got != oid:
        bad.append(f"bytes {path}")
    if not stat.S_ISREG(st.st_mode) or bool(st.st_mode & 0o111) != want_exec:
        bad.append(f"mode {path}")
for path in (p for p in blobs if entries[p][0] == "120000"):
    target = os.readlink(os.path.join(repo, path)).encode()
    got = subprocess.run(["git", "-C", repo, "hash-object", "--stdin"], input=target,
                         capture_output=True, env=env, check=True).stdout.decode().strip()
    if got != entries[path][2]:
        bad.append(f"symlink {path}")
links = {p: o for p, (m, k, o) in entries.items() if k == "commit"}
report = []
for path, oid in sorted(links.items()):
    sub = os.path.join(repo, path)
    try:
        got = git("rev-parse", "HEAD", cwd=sub).decode().strip()
        top = git("rev-parse", "--show-toplevel", cwd=sub).decode().strip()
        state = "initialised" if os.path.realpath(top) == os.path.realpath(sub) else "not-a-checkout"
    except subprocess.CalledProcessError:
        got, state = None, "uninitialised"
    report.append(f"{path} {oid} {state} {'match' if got == oid else got}")
    if state == "initialised" and got != oid:
        bad.append(f"gitlink {path}")
status = git("status", "--porcelain", "--ignored", "--untracked-files=all").decode().strip()
if status:
    bad.append(f"status: {status.splitlines()[:5]}")
print(f"HEAD {head} tree {tree}; {len(regular)} regular + {len(blobs) - len(regular)} symlink blobs proved; "
      f"{len(links)} gitlinks:")
for r in report:
    print("  ", r)
print("INTEGRITY", "FAIL " + "; ".join(bad[:10]) if bad else "PASS")
raise SystemExit(1 if bad else 0)

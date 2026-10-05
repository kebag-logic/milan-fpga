"""Verify a checkout against its exact head: every tracked blob's bytes and
mode equal the head tree's, the index equals the head tree, nothing is
untracked or ignored, and each required submodule sits at its gitlink with
the same checks inside it. Usage: verify_integrity.py <checkout> <head-sha>"""
import hashlib
import os
import stat
import subprocess
import sys

REQUIRED = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def blob_sha(path):
    st = os.lstat(path)
    data = os.readlink(path).encode() if stat.S_ISLNK(st.st_mode) else open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(), st.st_mode


def check(repo, commit, label):
    bad = []
    entries = git(repo, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0")
    blobs = gitlinks = 0
    links = {}
    for e in filter(None, entries):
        meta, path = e.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        path = path.decode()
        full = os.path.join(repo, path)
        if kind == "commit":
            gitlinks += 1
            links[path] = sha
            continue
        blobs += 1
        try:
            got, fmode = blob_sha(full)
        except OSError as exc:
            bad.append(f"{label}: {path}: {exc}")
            continue
        if got != sha:
            bad.append(f"{label}: {path}: bytes differ")
        want_mode = {"100644": 0o644, "100755": 0o755}.get(mode)
        if mode == "120000":
            if not stat.S_ISLNK(fmode):
                bad.append(f"{label}: {path}: not a symlink")
        elif bool(fmode & 0o111) != bool(want_mode & 0o111):
            bad.append(f"{label}: {path}: mode {oct(fmode)} want {mode}")
    tree = git(repo, "rev-parse", f"{commit}^{{tree}}").decode().strip()
    index_tree = git(repo, "write-tree").decode().strip()
    if index_tree != tree:
        bad.append(f"{label}: index tree {index_tree} != head tree {tree}")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    if head != git(repo, "rev-parse", commit).decode().strip():
        bad.append(f"{label}: HEAD {head} != {commit}")
    extra = git(repo, "status", "--porcelain", "--ignored", "--ignore-submodules=all").decode().strip()
    if extra:
        bad.append(f"{label}: untracked/ignored/modified: {extra[:400]}")
    print(f"{label}: head {head} tree {tree} blobs {blobs} gitlinks {gitlinks} findings {len(bad)}")
    return bad, links


repo, head = sys.argv[1], sys.argv[2]
bad, links = check(repo, head, "superproject")
for sub in REQUIRED:
    pin = links.get(sub)
    if pin is None:
        bad.append(f"{sub}: no gitlink")
        continue
    b, _ = check(os.path.join(repo, sub), pin, f"{sub}@{pin[:12]}")
    bad += b
for x in bad:
    print("FINDING", x)
print("INTEGRITY", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Verify a clone is byte-identical to its HEAD: tree, index, every tracked
blob rehashed, modes, gitlinks and submodule cleanliness."""
import os, stat, subprocess, sys
C = sys.argv[1]  # the review clone
def git(*a, inp=None):
    return subprocess.run(["git", "-C", C, *a], input=inp, capture_output=True, check=True).stdout
print("HEAD=" + git("rev-parse", "HEAD").decode().strip())
print("HEAD_TREE=" + git("rev-parse", "HEAD^{tree}").decode().strip())
print("INDEX_TREE=" + git("write-tree").decode().strip())
st = git("status", "--porcelain", "--ignore-submodules=none").decode()
print(f"status_porcelain_lines={len(st.splitlines())}"); print(st, end="")
bad = n = 0
for rec in git("ls-files", "-s", "-z").split(b"\0"):
    if not rec: continue
    meta, path = rec.split(b"\t", 1); mode, sha, _stage = meta.decode().split()
    p = os.path.join(C, path.decode()); n += 1
    if mode == "160000": continue
    if mode == "120000":
        data = os.readlink(p).encode()
        got = git("hash-object", "--stdin", inp=data).decode().strip()
    else:
        got = git("hash-object", "--no-filters", p).decode().strip()
        x = bool(os.stat(p).st_mode & stat.S_IXUSR)
        if x != (mode == "100755"):
            print("MODE MISMATCH", path.decode()); bad += 1
    if got != sha:
        print("BLOB MISMATCH", path.decode()); bad += 1
print(f"tracked_entries={n} blob_or_mode_mismatches={bad}")
print("gitlinks:")
for line in git("ls-tree", "-r", "HEAD").decode().splitlines():
    m, t, s, path = line.split(None, 3)
    if t == "commit": print(s, path)
print("submodule status:"); print(git("submodule", "status").decode(), end="")
for sm in ("gptp-processor", "protocol-processor", "third_party/verilog-axis"):
    d = subprocess.run(["git", "-C", os.path.join(C, sm), "status", "--porcelain"], capture_output=True).stdout.decode()
    print(f"submodule {sm} dirty_lines={len(d.splitlines())}")

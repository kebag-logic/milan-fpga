#!/usr/bin/env python3
"""Exact-head integrity of a review clone, independent of the code under review.

Records HEAD, tree, raw index digest, every tracked non-gitlink path's on-disk
Git blob id (hashed here from raw bytes, no filters) and exact st_mode, whether
it equals the HEAD record, assume-unchanged/skip-worktree flags, untracked
files, and the three required submodule gitlinks against their checkouts.
Usage: integrity.py CLONE OUT.json
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

clone = Path(sys.argv[1]); out = Path(sys.argv[2])
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
def git(*a, cwd=clone):
    return subprocess.run(["git", "--no-replace-objects", "-C", str(cwd), *a], env=env,
                          check=True, capture_output=True).stdout
head = git("rev-parse", "HEAD").decode().strip()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
index = git("ls-files", "--stage", "-z")
headtree = {}
for row in git("ls-tree", "-rz", "HEAD").split(b"\0"):
    if row:
        meta, name = row.split(b"\t", 1); mode, kind, obj = meta.split(b" ")
        headtree[name.decode()] = (mode.decode(), obj.decode())
mismatch = []; files = 0
for row in index.split(b"\0"):
    if not row: continue
    meta, name = row.split(b"\t", 1); mode, obj, stage = meta.decode().split(" "); name = name.decode()
    if headtree.get(name) != (mode, obj) or stage != "0":
        mismatch.append(("index-vs-HEAD", name))
    if mode == "160000": continue
    p = clone / name
    try:
        st = p.lstat()
    except FileNotFoundError:
        mismatch.append(("missing", name)); continue
    files += 1
    data = os.readlink(p).encode() if (st.st_mode & 0o170000) == 0o120000 else p.read_bytes()
    blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    want_mode = {"100644": 0o100644, "100755": 0o100755, "120000": 0o120000}[mode]
    kind_ok = (st.st_mode & 0o170000) == (want_mode & 0o170000)
    exec_ok = mode == "120000" or bool(st.st_mode & 0o100) == (mode == "100755")
    if blob != obj or not kind_ok or not exec_ok:
        mismatch.append(("worktree-vs-index", name, blob, obj, oct(st.st_mode)))
flags = [l for l in git("ls-files", "-v").decode().splitlines() if l[:1] in "abcdefghijklmnopqrstuvwxyzS" and not l.startswith("H ")]
untracked = git("ls-files", "--others", "--exclude-standard").decode().splitlines()
ignored = git("ls-files", "--others", "--ignored", "--exclude-standard", "--directory").decode().splitlines()
subs = {}
for sm in ("gptp-processor", "protocol-processor", "third_party/verilog-axis"):
    pin = headtree.get(sm)
    chk = git("rev-parse", "HEAD", cwd=clone / sm).decode().strip()
    dirty = git("status", "--porcelain", cwd=clone / sm).decode()
    subs[sm] = dict(pin=pin, checkout=chk, match=pin == ("160000", chk), dirty=dirty)
result = dict(head=head, tree=tree, index_sha256=hashlib.sha256(index).hexdigest(),
              tracked_files_hashed=files, mismatches=mismatch, flagged=flags,
              untracked=untracked, ignored=ignored, submodules=subs,
              clean=not mismatch and not flags and not untracked and all(s["match"] and not s["dirty"] for s in subs.values()))
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: result[k] for k in ("head", "tree", "index_sha256", "tracked_files_hashed", "clean")}))
print("mismatches:", mismatch[:10]); print("untracked:", untracked[:10]); print("ignored:", ignored[:20])

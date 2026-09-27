#!/usr/bin/env python3
"""Verify every tracked non-gitlink entry's worktree bytes and mode against
HEAD's tree (blob id recomputed from the bytes on disk, no index shortcuts),
and every gitlink's checkout HEAD against the recorded commit.
Usage: verify_tracked_bytes.py <repo>"""
import hashlib
import os
import subprocess
import sys

repo = sys.argv[1]
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "HEAD"],
                     capture_output=True, check=True, env=env).stdout
bad = n = links = 0
for rec in out.split(b"\0"):
    if not rec:
        continue
    meta, path = rec.split(b"\t", 1)
    mode, _typ, oid = meta.decode().split()
    full = os.path.join(repo.encode(), path)
    if mode == "160000":
        links += 1
        if not os.path.exists(os.path.join(full, b".git")):
            print("UNINITIALISED GITLINK (not required)", path.decode(), oid)
            continue
        head = subprocess.run(["git", "-C", full, "rev-parse", "HEAD"],
                              capture_output=True, text=True, env=env).stdout.strip()
        if head != oid:
            print("GITLINK MISMATCH", path.decode(), head, oid); bad += 1
        continue
    n += 1
    if mode == "120000":
        data = os.readlink(full)
        ok_mode = os.path.islink(full)
    else:
        if os.path.islink(full) or not os.path.isfile(full):
            print("TYPE MISMATCH", path.decode()); bad += 1; continue
        with open(full, "rb") as fh:
            data = fh.read()
        exe = bool(os.stat(full).st_mode & 0o100)
        ok_mode = exe == (mode == "100755")
    got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if got != oid or not ok_mode:
        print("MISMATCH", mode, path.decode(), got, oid, "mode_ok" if ok_mode else "mode_bad")
        bad += 1
print(f"checked {n} tracked blobs and {links} gitlinks: "
      + ("ALL MATCH HEAD" if not bad else f"{bad} MISMATCH(ES)"))
sys.exit(1 if bad else 0)

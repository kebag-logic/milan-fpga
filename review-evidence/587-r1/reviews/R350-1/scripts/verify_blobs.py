#!/usr/bin/env python3
"""Re-hash every tracked blob in the working tree and compare bytes and modes with the index."""
import hashlib, os, stat, subprocess, sys
out = subprocess.run(["git", "ls-files", "-s", "-z"], capture_output=True, check=True).stdout
bad = n = 0
for entry in out.split(b"\0"):
    if not entry:
        continue
    meta, path = entry.split(b"\t", 1)
    mode, sha, _stage = meta.split()
    if mode == b"160000":
        continue
    n += 1
    p = os.fsdecode(path)
    st = os.lstat(p)
    if mode == b"120000":
        data = os.fsencode(os.readlink(p)); ok_mode = stat.S_ISLNK(st.st_mode)
    else:
        data = open(p, "rb").read()
        want_exec = mode == b"100755"
        ok_mode = stat.S_ISREG(st.st_mode) and bool(st.st_mode & 0o111) == want_exec
    got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest().encode()
    if got != sha or not ok_mode:
        bad += 1
        print(f"MISMATCH {p} mode={mode.decode()} ok_mode={ok_mode}")
print(f"tracked blobs rehashed={n} mismatches={bad}")
sys.exit(1 if bad else 0)

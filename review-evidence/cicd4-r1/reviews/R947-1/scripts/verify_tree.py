#!/usr/bin/env python3
"""Re-hash every tracked file of a checkout against its index entry (blob id and mode), and report each
initialized submodule's checked-out commit and cleanliness. Usage: verify_tree.py <checkout> <expected-head>"""
import os
import stat
import subprocess
import sys

repo, head = sys.argv[1], sys.argv[2]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
assert git("rev-parse", "HEAD").strip() == head, "HEAD differs"
bad, n, links = [], 0, []
for line in git("ls-files", "-s", "-z").split("\0"):
    if not line:
        continue
    meta, path = line.split("\t", 1)
    mode, blob, _ = meta.split()
    full = os.path.join(repo, path)
    if mode == "160000":
        links.append((path, blob))
        continue
    n += 1
    st = os.lstat(full)
    if mode == "120000":
        ok = stat.S_ISLNK(st.st_mode)
        got = subprocess.run(["git", "hash-object", "--stdin"], input=os.readlink(full).encode(),
                             capture_output=True, check=True).stdout.decode().strip()
    else:
        ok = stat.S_ISREG(st.st_mode) and (bool(st.st_mode & 0o111) == (mode == "100755"))
        got = subprocess.run(["git", "hash-object", full], capture_output=True, check=True, text=True).stdout.strip()
    if not ok or got != blob:
        bad.append(path)
print(f"tracked files re-hashed: {n}; mismatched blob or mode: {len(bad)} {bad[:10]}")
for path, blob in links:
    sub = os.path.join(repo, path)
    if not os.path.exists(os.path.join(sub, ".git")):
        print(f"gitlink {path} {blob}: not initialized")
        continue
    cur = subprocess.run(["git", "-C", sub, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", sub, "status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True).stdout.strip()
    print(f"gitlink {path} {blob}: checked out {cur} {'MATCH' if cur == blob else 'DIFFERS'}; "
          f"tracked changes: {'none' if not dirty else dirty[:200]}")
print("RESULT:", "PASS" if not bad else "FAIL")

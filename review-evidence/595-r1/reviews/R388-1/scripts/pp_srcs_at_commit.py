#!/usr/bin/env python3
"""Run scripts/pp_srcs.py's literal-source check against the tracked blobs of
a commit (read with git show), without checking the commit out.
Usage: pp_srcs_at_commit.py <repo> <commit>"""
import subprocess, sys
repo, rev = sys.argv[1], sys.argv[2]
sys.path.insert(0, f"{repo}/scripts")
import pp_srcs
files = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                       capture_output=True, text=True, check=True).stdout.split()
def read(f):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{f}"], capture_output=True)
    if r.returncode:
        raise OSError(f)
    return r.stdout.decode()
bad, ok = pp_srcs.check(files, read)
print(f"{rev}: {len(bad)} finding(s), {len(ok)} permitted-prose file(s)")
for b in bad:
    print(" ", b[:300])
sys.exit(1 if bad else 0)

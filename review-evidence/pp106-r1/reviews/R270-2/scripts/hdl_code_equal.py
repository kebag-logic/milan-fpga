#!/usr/bin/env python3
"""Show that two commits' hdl/ trees differ only in comments: strip // and
/* */ comments and whitespace, then compare every .sv file.
usage: hdl_code_equal.py <repo> <rev-a> <rev-b>"""
import re, subprocess, sys
repo, a, b = sys.argv[1:4]
def files(rev):
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "hdl/"],
                         capture_output=True, text=True, check=True).stdout.split()
    return [f for f in out if f.endswith((".sv", ".svh", ".v"))]
def code(rev, f):
    t = subprocess.run(["git", "-C", repo, "show", f"{rev}:{f}"], capture_output=True,
                       text=True, check=True).stdout
    t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
    t = re.sub(r"//[^\n]*", " ", t)
    return re.sub(r"\s+", " ", t).strip()
fa, fb = set(files(a)), set(files(b))
rc = 0
if fa != fb:
    print("file sets differ:", sorted(fa ^ fb)); rc = 1
for f in sorted(fa & fb):
    ca, cb = code(a, f), code(b, f)
    raw = subprocess.run(["git", "-C", repo, "diff", "--quiet", a, b, "--", f]).returncode
    if ca != cb:
        print(f"CODE DIFFERS {f}"); rc = 1
    elif raw:
        print(f"comment-only change {f}")
print(f"{len(fa & fb)} hdl files compared {a[:8]}..{b[:8]}: {'code identical' if rc == 0 else 'CODE CHANGED'}")
sys.exit(rc)

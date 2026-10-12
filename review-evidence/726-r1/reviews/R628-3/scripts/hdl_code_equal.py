#!/usr/bin/env python3
"""Compare HDL files between two commits with // and /* */ comments and blank
lines removed. Usage: hdl_code_equal.py REPO OLD NEW"""
import re, subprocess, sys
repo, old, new = sys.argv[1:4]
def strip(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"//.*", "", t)
    return [l.rstrip() for l in t.splitlines() if l.strip()]
files = subprocess.check_output(["git", "diff", "--name-only", old, new, "--", "hdl"], cwd=repo, text=True).split()
rc = 0
for f in files:
    a = strip(subprocess.check_output(["git", "show", f"{old}:{f}"], cwd=repo, text=True))
    b = strip(subprocess.check_output(["git", "show", f"{new}:{f}"], cwd=repo, text=True))
    print(("code-equal  " if a == b else "CODE-DIFF   ") + f)
    rc |= a != b
sys.exit(rc)

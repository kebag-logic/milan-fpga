#!/usr/bin/env python3
"""[R453-2] Compare two git revisions' HDL with SystemVerilog comments stripped.
Usage: strip_compare.py REPO REV_A REV_B  (prints EQUAL/DIFF per changed .sv/.svh file)"""
import re, subprocess, sys
repo, a, b = sys.argv[1:4]
def show(rev, p):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{p}"], capture_output=True, text=True, check=True).stdout
def strip(t):
    t = re.sub(r"/\*.*?\*/", " ", t, flags=re.S)
    t = re.sub(r"//[^\n]*", "", t)
    return [l.rstrip() for l in t.splitlines() if l.strip()]
names = subprocess.run(["git", "-C", repo, "diff", "--name-only", a, b, "--", "hdl", "syn"], capture_output=True, text=True, check=True).stdout.split()
rc = 0
for p in names:
    eq = strip(show(a, p)) == strip(show(b, p))
    rc |= not eq
    print(("EQUAL " if eq else "DIFF  ") + p)
sys.exit(rc)

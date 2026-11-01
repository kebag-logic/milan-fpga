#!/usr/bin/env python3
"""Compare two AX7101 exports with comments and timestamps removed. usage: cmp_export.py <a.v> <b.v>"""
import difflib, hashlib, re, sys
def strip(p):
    t = open(p).read()
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    out = []
    for l in t.split("\n"):
        l = re.sub(r"//.*$", "", l).rstrip()
        if l.strip():
            out.append(l)
    return out
TREE = re.compile(r"\S*/scratch/cl_[a-z0-9]+/")
a, b = [[TREE.sub("<tree>/", l) for l in strip(p)] for p in sys.argv[1:3]]
print(f"{sys.argv[1].split('/')[-4]} lines {len(a)} sha256 {hashlib.sha256(chr(10).join(a).encode()).hexdigest()}")
print(f"{sys.argv[2].split('/')[-4]} lines {len(b)} sha256 {hashlib.sha256(chr(10).join(b).encode()).hexdigest()}")
d = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if not l.startswith(("---", "+++", "@@"))]
print("IDENTICAL" if a == b else f"DIFFERS, {len(d)} changed lines")
for l in d[:40]:
    print("   ", l[:150])

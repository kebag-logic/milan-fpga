#!/usr/bin/env python3
"""strip_cmp.py A B ROOT_A ROOT_B: compare two Verilog texts, comments and blank lines removed, each tree's own root path normalised."""
import hashlib, re, sys
def clean(p, root):
    t = open(p).read().replace(root, "<TREE>")
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"(?<!:)//[^\n]*", "", t)
    return "\n".join(l.rstrip() for l in t.splitlines() if l.strip()) + "\n"
a, b = clean(sys.argv[1], sys.argv[3]), clean(sys.argv[2], sys.argv[4])
for p, t in zip(sys.argv[1:3], (a, b)):
    print(len(t.splitlines()), "lines", hashlib.sha256(t.encode()).hexdigest())
print("VERDICT:", "IDENTICAL" if a == b and a else "DIFFERENT")

#!/usr/bin/env python3
"""Classify every path of a two-parent merge: base/ours/theirs/result (mode+oid incl. gitlinks)."""
import subprocess, sys
repo, base, ours, theirs, res = sys.argv[1:6]
def tree(c):
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "--full-tree", c], capture_output=True, check=True).stdout
    d = {}
    for rec in out.split(b"\0"):
        if not rec: continue
        meta, path = rec.split(b"\t", 1)
        mode, typ, oid = meta.split()
        d[path.decode()] = (mode.decode(), oid.decode())
    return d
B, O, T, R = (tree(c) for c in (base, ours, theirs, res))
counts = {}
bad = []
for p in sorted(set(B) | set(O) | set(T) | set(R)):
    b, o, t, r = B.get(p), O.get(p), T.get(p), R.get(p)
    if o == t: exp, kind = o, "same-both"
    elif o == b: exp, kind = t, "theirs-only"
    elif t == b: exp, kind = o, "ours-only"
    else: exp, kind = "BOTH", "both-changed"
    counts[kind] = counts.get(kind, 0) + 1
    if exp == "BOTH":
        print(f"BOTH-CHANGED {p}: result={'ours' if r==o else 'theirs' if r==t else 'new'} {r}")
    elif r != exp:
        bad.append(p); print(f"MISMATCH {kind} {p}: expected {exp} got {r}")
print({k: counts[k] for k in sorted(counts)})
print(f"mismatches: {len(bad)}")
sys.exit(1 if bad else 0)

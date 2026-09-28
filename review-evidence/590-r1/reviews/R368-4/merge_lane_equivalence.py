#!/usr/bin/env python3
"""Check a merge resolution keeps both lanes' changes to one file unchanged.

For file F, merge M with parents P1 (lane) and P2 (dev) and merge base B:
the edit P1->M must equal the edit B->P2 and the edit P2->M must equal B->P1,
compared as ordered sequences of removed and added lines (context-free).
Usage: merge_lane_equivalence.py <repo> <file> <B> <P1> <P2> <M>
"""
import difflib, subprocess, sys

def blob(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True).stdout.decode().splitlines()

def edits(a, b):
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            out.append((tuple(a[i1:i2]), tuple(b[j1:j2])))
    return out

repo, path, B, P1, P2, M = sys.argv[1:7]
b, p1, p2, m = (blob(repo, r, path) for r in (B, P1, P2, M))
ok = True
for name, x, y in (("P1->M == B->P2", edits(p1, m), edits(b, p2)),
                   ("P2->M == B->P1", edits(p2, m), edits(b, p1))):
    same = x == y
    ok &= same
    print(f"{name}: {'EQUAL' if same else 'DIFFERENT'} ({len(x)} vs {len(y)} edit blocks)")
    if not same:
        for i, (u, v) in enumerate(zip(x, y)):
            if u != v:
                print("  first differing block", i); print("  merge:", u); print("  lane: ", v); break
sys.exit(0 if ok else 1)

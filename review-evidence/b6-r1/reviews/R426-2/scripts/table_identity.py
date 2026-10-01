#!/usr/bin/env python3
"""Compare every Markdown table of a page between two commits, byte for byte.
Usage: table_identity.py <repo> <base> <head> <path>"""
import hashlib, subprocess, sys
repo, base, head, path = sys.argv[1:5]
def tables(rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode()
    out, cur = [], []
    for line in text.split("\n"):
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append("\n".join(cur)); cur = []
    if cur: out.append("\n".join(cur))
    return out
tb, th = tables(base), tables(head)
print(f"tables base={len(tb)} head={len(th)}")
ok = len(tb) == len(th)
for i, (a, b) in enumerate(zip(tb, th)):
    ha, hb = hashlib.sha256(a.encode()).hexdigest(), hashlib.sha256(b.encode()).hexdigest()
    same = a == b
    ok &= same
    print(f"table {i+1:2d} lines={a.count(chr(10))+1:3d} base={ha[:16]} head={hb[:16]} {'EQUAL' if same else 'DIFFERENT'}")
allb, allh = "\n".join(tb), "\n".join(th)
print("all-table-lines sha256 base", hashlib.sha256(allb.encode()).hexdigest(), "bytes", len(allb.encode()), "lines", allb.count("\n")+1)
print("all-table-lines sha256 head", hashlib.sha256(allh.encode()).hexdigest(), "bytes", len(allh.encode()), "lines", allh.count("\n")+1)
print("RESULT", "IDENTICAL" if ok else "CHANGED")
sys.exit(0 if ok else 1)

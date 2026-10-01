#!/usr/bin/env python3
"""Compare every Markdown table of a page between two commits (reviewer-written).
usage: r425_tables.py <repo> <old rev> <new rev> <path>"""
import hashlib, subprocess, sys
repo, old, new, path = sys.argv[1:5]
def tables(rev):
    txt = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, check=True).stdout.decode()
    out, cur = [], []
    for line in txt.split("\n"):
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out
a, b = tables(old), tables(new)
print(f"tables: {old[:8]} {len(a)}, {new[:8]} {len(b)}; table lines {sum(map(len,a))} -> {sum(map(len,b))}")
same = 0
for i, (x, y) in enumerate(zip(a, b), 1):
    hx = hashlib.sha256("\n".join(x).encode()).hexdigest()[:16]
    hy = hashlib.sha256("\n".join(y).encode()).hexdigest()[:16]
    eq = x == y
    same += eq
    print(f"table {i:2d} header {x[0][:50]!r}: {len(x)} lines, {hx} -> {hy} {'IDENTICAL' if eq else 'CHANGED'}")
    if not eq:
        for j, (lx, ly) in enumerate(zip(x, y)):
            if lx != ly:
                cx, cy = lx.split(" | "), ly.split(" | ")
                diffcells = [k for k in range(max(len(cx), len(cy))) if (cx[k] if k < len(cx) else None) != (cy[k] if k < len(cy) else None)]
                print(f"   row {j}: cells {len(cx)}->{len(cy)}; changed cell indices {diffcells}; first cell {cx[0]!r}; verdict cell {cx[1]!r} -> {cy[1]!r}")
print(f"identical {same} of {len(a)}")

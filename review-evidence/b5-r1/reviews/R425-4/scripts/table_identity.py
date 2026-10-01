#!/usr/bin/env python3
"""Table identity of the B5 findings page between commits (label-only for old cells).

usage: table_identity.py <repo> <rev-a> <rev-b> [<rev-a> <rev-b> ...]

A table is a maximal run of lines starting with '|'. Tables are matched by
ordinal and by header line. For each changed line the changed cell ordinals are
printed with the old cell's SHA-256 prefix (never its text, which may carry a
value the public-text rule removed) and the new cell's text.
"""
import hashlib, subprocess, sys

PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
def tables(repo, rev):
    t = subprocess.run(["git", "-C", repo, "show", f"{rev}:{PAGE}"], capture_output=True,
                       text=True, check=True).stdout.split("\n")
    out, cur = [], []
    for ln in t:
        if ln.startswith("|"):
            cur.append(ln)
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out
h = lambda s: hashlib.sha256(s.encode()).hexdigest()
repo = sys.argv[1]
pairs = sys.argv[2:]
for a, b in zip(pairs[::2], pairs[1::2]):
    ta, tb = tables(repo, a), tables(repo, b)
    same = 0
    print(f"== {a[:8]} -> {b[:8]}: {len(ta)} tables -> {len(tb)} tables, "
          f"{sum(map(len, ta))} -> {sum(map(len, tb))} table lines")
    for i, (x, y) in enumerate(zip(ta, tb), 1):
        if x == y:
            same += 1
            print(f"  table {i:2d} identical  {h(chr(10).join(x))[:16]}  {x[0][:60]}")
            continue
        print(f"  table {i:2d} CHANGED    {x[0][:60]}")
        for j, (lx, ly) in enumerate(zip(x, y)):
            if lx != ly:
                cx, cy = lx.split("|"), ly.split("|")
                diffc = [k for k in range(max(len(cx), len(cy)))
                         if (cx[k] if k < len(cx) else None) != (cy[k] if k < len(cy) else None)]
                for k in diffc:
                    print(f"     line {j}: cell {k} old sha256 {h(cx[k])[:16] if k < len(cx) else '-'}"
                          f" -> new: {cy[k].strip() if k < len(cy) else '-'}")
                print(f"     line {j}: first cell unchanged: {cx[1] == cy[1]} ({cy[1].strip()})")
        if len(x) != len(y):
            print(f"     row count {len(x)} -> {len(y)}")
    print(f"  identical {same} of {len(tb)}")

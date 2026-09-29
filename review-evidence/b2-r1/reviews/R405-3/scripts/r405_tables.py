#!/usr/bin/env python3
"""R405-2: compare every Markdown table between two revisions of a page (or two
files), keyed by the table's header line, and report identical / changed /
added / removed tables with a line diff for changed ones.
Usage: r405_tables.py <old-file> <new-file>"""
import difflib, sys

def tables(path):
    out, cur = [], []
    for line in open(path, encoding="utf-8").read().splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

old, new = tables(sys.argv[1]), tables(sys.argv[2])
ok = {t[0]: t for t in old}; nk = {t[0]: t for t in new}
same = changed = 0
for h, t in nk.items():
    if h not in ok:
        print("ADDED  ", h[:110], f"({len(t)} lines)"); continue
    if ok[h] == t:
        same += 1; print("SAME   ", h[:110], f"({len(t)} lines)")
    else:
        changed += 1; print("CHANGED", h[:110])
        for d in difflib.unified_diff(ok[h], t, lineterm="", n=0):
            print("    ", d)
for h in ok:
    if h not in nk: print("REMOVED", h[:110])
print(f"summary: old {len(old)} tables, new {len(new)} tables, identical {same}, changed {changed}")

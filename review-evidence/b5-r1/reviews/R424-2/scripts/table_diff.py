#!/usr/bin/env python3
"""Reviewer-side table comparison of the B5 page between two revisions.

usage: table_diff.py <repo> <old_rev> <new_rev>

A table is a maximal run of lines starting with '|'. Tables are paired in
order; each pair is compared byte for byte, and for a changed table every
changed cell is printed with its row and column header.
"""
import subprocess
import sys

REPO, OLD, NEW = sys.argv[1:4]
PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"


def blocks(rev):
    txt = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{PAGE}"], check=True,
                         capture_output=True).stdout.decode()
    out, cur = [], []
    for line in txt.split("\n"):
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def split(row):
    return [c.strip() for c in row.strip()[1:-1].split("|")]


old, new = blocks(OLD), blocks(NEW)
print(f"tables {len(old)} -> {len(new)}")
same = 0
for i, (a, b) in enumerate(zip(old, new), 1):
    if a == b:
        same += 1
        continue
    print(f"table {i} CHANGED ({len(a)} -> {len(b)} lines); header {split(a[0])}")
    hdr = split(a[0])
    for r, (x, y) in enumerate(zip(a, b)):
        if x != y:
            cx, cy = split(x), split(y)
            for c, (u, v) in enumerate(zip(cx, cy)):
                if u != v:
                    print(f"  row {r} [{cx[0]}] column '{hdr[c]}':\n    old: {u}\n    new: {v}")
            if len(cx) != len(cy):
                print(f"  row {r}: cell count {len(cx)} -> {len(cy)}")
print(f"{same} of {len(old)} tables byte-identical")

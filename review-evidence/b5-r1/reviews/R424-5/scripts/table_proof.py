#!/usr/bin/env python3
"""Compare the findings page's Markdown tables between two revisions.

Usage: table_proof.py <old.md> <new.md>
Tables are maximal runs of lines starting with '|', compared in order. For a
table that differs, the cells that differ are named by row label and column
header only; no old cell text is printed.
"""
import sys


def tables(path):
    out, cur = [], []
    for line in open(path, encoding="utf-8").read().splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main(old, new):
    a, b = tables(old), tables(new)
    print(f"tables: old {len(a)} ({sum(map(len, a))} lines), new {len(b)} ({sum(map(len, b))} lines)")
    same = 0
    for i, (x, y) in enumerate(zip(a, b), 1):
        head = cells(x[0])[0]
        if x == y:
            same += 1
            print(f"table {i:2} '{head}': byte-identical, {len(x)} lines")
            continue
        print(f"table {i:2} '{head}': DIFFERS ({len(x)} -> {len(y)} lines)")
        hdr = cells(x[0])
        if len(x) != len(y):
            print("  row count changed")
            continue
        for rx, ry in zip(x, y):
            if rx != ry:
                cx, cy = cells(rx), cells(ry)
                if len(cx) != len(cy):
                    print(f"  row '{cx[0]}': column count changed")
                    continue
                cols = [hdr[k] if k < len(hdr) else str(k) for k in range(len(cx)) if cx[k] != cy[k]]
                print(f"  row '{cx[0]}': cells changed in column(s) {cols}")
    print(f"byte-identical: {same} of {min(len(a), len(b))}")


if __name__ == "__main__":
    main(*sys.argv[1:3])

#!/usr/bin/env python3
"""Compare every Markdown table of a page between two commits, byte for byte.

usage: table_diff.py <repo> <base_rev> <head_rev> <page> [<page> ...]

A table is a maximal run of lines that start with '|'. Tables are paired in
order of appearance; each pair is reported as IDENTICAL with the SHA-256 of
its bytes, or CHANGED with every differing line. The exit status is 0 when
both commits hold the same number of tables per page, whatever changed, so
the output is the evidence and a reader decides; it is 2 on a count mismatch.
"""
import difflib
import hashlib
import subprocess
import sys


def tables(text):
    out, cur, start = [], [], None
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("|"):
            if not cur:
                start = n
            cur.append(line)
        elif cur:
            out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out


def show(repo, rev, page):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], check=True,
                          capture_output=True).stdout.decode()


def main():
    repo, base, head, pages = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    rc = 0
    for page in pages:
        a, b = tables(show(repo, base, page)), tables(show(repo, head, page))
        same = sum(1 for x, y in zip(a, b) if x[1] == y[1])
        print(f"== {page}: {len(a)} tables at {base}, {len(b)} at {head}; {same} identical")
        if len(a) != len(b):
            rc = 2
        for i, (x, y) in enumerate(zip(a, b), 1):
            bx = ("\n".join(x[1]) + "\n").encode()
            by = ("\n".join(y[1]) + "\n").encode()
            if bx == by:
                print(f"  table {i}: IDENTICAL, lines {x[0]}-{x[0] + len(x[1]) - 1} -> {y[0]}-{y[0] + len(y[1]) - 1}, "
                      f"{len(bx)} bytes, sha256 {hashlib.sha256(bx).hexdigest()}")
            else:
                print(f"  table {i}: CHANGED, lines {x[0]}-{x[0] + len(x[1]) - 1} -> {y[0]}-{y[0] + len(y[1]) - 1}, "
                      f"{len(bx)} -> {len(by)} bytes")
                for d in difflib.unified_diff(x[1], y[1], lineterm="", n=0):
                    if not d.startswith(("---", "+++", "@@")):
                        print(f"    {d}")
    sys.exit(rc)


if __name__ == "__main__":
    main()

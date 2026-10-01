#!/usr/bin/env python3
"""Prove the B6 page's tables byte-identical between two commits (read-only).

usage: table_identity.py <repo> <old_commit> <new_commit> <path>

A table is a maximal run of lines starting with "|". Each table of the old page must
appear in the new page byte for byte and in the same order, and the new page may hold
no table the old one lacks. Exit 0 only then.
"""
import hashlib
import subprocess
import sys

repo, old_c, new_c, path = sys.argv[1:5]


def show(c):
    return subprocess.run(["git", "-C", repo, "show", f"{c}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def tables(text):
    out, cur, start = [], [], None
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("|"):
            if not cur:
                start = i
            cur.append(line)
        elif cur:
            out.append((start + 1, "\n".join(cur) + "\n"))
            cur = []
    if cur:
        out.append((start + 1, "\n".join(cur) + "\n"))
    return out


old, new = tables(show(old_c)), tables(show(new_c))
print(f"{path}: {len(old)} tables at {old_c[:12]}, {len(new)} at {new_c[:12]}")
ok = len(old) == len(new)
for (lo, to), (ln, tn) in zip(old, new):
    same = to == tn
    ok &= same
    print(f"  table old line {lo:4d} -> new line {ln:4d}: {to.count(chr(10)):2d} rows, "
          f"{len(to.encode()):5d} bytes, sha256 {hashlib.sha256(to.encode()).hexdigest()[:16]} "
          f"{'IDENTICAL' if same else 'DIFFERENT'}")
print("RESULT", "PASS: every table byte-identical, none added or removed" if ok else "FAIL")
sys.exit(0 if ok else 1)

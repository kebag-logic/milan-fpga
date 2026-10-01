#!/usr/bin/env python3
"""Compare every Markdown table line of the #451 timing page between two commits.

usage: table_identity.py <repo> <old_rev> <new_rev>
Prints each table (by position) and whether its lines are byte-identical.
"""
import subprocess, sys, hashlib
repo, old, new = sys.argv[1:4]
PATH = "docs/findings/451_TDM8_TIMING_SOC_BOARD.md"

def tables(rev):
    b = subprocess.run(["git", "-C", repo, "show", f"{rev}:{PATH}"], capture_output=True, check=True).stdout
    out, cur, start = [], [], None
    for i, line in enumerate(b.split(b"\n"), 1):
        if line.startswith(b"|"):
            if not cur: start = i
            cur.append(line)
        elif cur:
            out.append((start, cur)); cur = []
    if cur: out.append((start, cur))
    return out

to, tn = tables(old), tables(new)
print(f"tables: old={len(to)} new={len(tn)}")
diffs = 0
for k, ((so, lo), (sn, ln)) in enumerate(zip(to, tn)):
    same = lo == ln
    h = hashlib.sha256(b"\n".join(ln)).hexdigest()[:16]
    print(f"table {k}: old line {so} new line {sn} rows {len(ln)} identical={same} sha256[:16]={h} header={ln[0][:60]!r}")
    if not same:
        for a, b in zip(lo, ln):
            if a != b:
                diffs += 1
                print("  OLD:", a.decode()); print("  NEW:", b.decode())
print("differing table lines:", diffs)

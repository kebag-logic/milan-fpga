#!/usr/bin/env python3
"""Compare the Markdown tables of the B5 findings page across three heads.

usage: table_identity.py <repo>
A table is a maximal run of lines starting with '|'. Prints per-table SHA-256 at
each head, identity verdicts, and the changed cells of any table that differs.
"""
import hashlib, subprocess, sys

PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
HEADS = [("r1", "bf9e5d82a401d167a8ffc786677a19dc7aac0cf2"),
         ("r2", "e29d12b1d5ee858eaf4684aaa8dc6647f6309857"),
         ("r3", "cf38633ad9a5bdb05517bedba73ce50965af967b")]

def tables(repo, rev):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{PAGE}"], check=True,
                          capture_output=True).stdout.decode()
    out, cur = [], []
    for line in text.split("\n"):
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out

def h(t):
    return hashlib.sha256(("\n".join(t) + "\n").encode()).hexdigest()

repo = sys.argv[1]
T = {k: tables(repo, rev) for k, rev in HEADS}
for k, _ in HEADS:
    print(f"{k}: {len(T[k])} tables, {sum(len(t) for t in T[k])} table lines")
n = len(T["r3"])
assert all(len(T[k]) == n for k in T), "table count differs"
same_r2 = same_r1 = 0
for i in range(n):
    a, b, c = T["r1"][i], T["r2"][i], T["r3"][i]
    s12, s23 = h(b) == h(c), h(a) == h(c)
    same_r2 += s12; same_r1 += s23
    print(f"table {i+1:2d} lines {len(c):3d} r3 {h(c)[:16]} same-as-r2 {s12} same-as-r1 {s23} header {c[0][:60]!r}")
    if not s12:
        for j, (x, y) in enumerate(zip(b, c)):
            if x != y:
                xc, yc = x.split(" | "), y.split(" | ")
                for ci, (u, v) in enumerate(zip(xc, yc)):
                    if u != v:
                        print(f"   r2->r3 changed: row {j} cell {ci}\n     r2: {u}\n     r3: {v}")
                if len(xc) != len(yc):
                    print("   cell count differs")
        if len(b) != len(c):
            print("   row count differs")
print(f"identical to r2: {same_r2} of {n}; identical to r1: {same_r1} of {n}")

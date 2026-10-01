#!/usr/bin/env python3
"""Prove which Markdown tables of the B5 page changed between two revisions.

usage: b5_table_proof.py <repo> <old_rev> <new_rev>

Every table (a run of lines starting with "|") of docs/findings/117_AUDIO_CONTINUITY.md
is taken at both revisions, in order, and compared byte for byte by SHA-256. For a
table that differs, every changed row is listed with its cells. For a changed row,
the first columns (the item and verdict cells) are compared, and every number of the
old row is looked for in the new row, so a wording change that drops or alters a
figure shows. The index row in docs/findings/README.md is reported the same way.
"""
import hashlib
import re
import subprocess
import sys

REPO, OLD, NEW = sys.argv[1:4]
PAGE = "docs/findings/117_AUDIO_CONTINUITY.md"
INDEX = "docs/findings/README.md"
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def show(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def tables(text):
    out, cur, start = [], [], 0
    for i, line in enumerate(text.split("\n"), 1):
        if line.startswith("|"):
            if not cur:
                start = i
            cur.append(line)
        elif cur:
            out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out


def h(lines):
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def compare_rows(old, new, keep):
    res = []
    for k, (a, b) in enumerate(zip(old, new)):
        if a == b:
            continue
        ca, cb = cells(a), cells(b)
        same_lead = ca[:keep] == cb[:keep]
        na, nb = NUM.findall(" ".join(ca[keep:])), NUM.findall(" ".join(cb[keep:]))
        missing = [n for n in na if n not in nb]
        res.append(f"  row {k + 1}: first {keep} cells {'identical' if same_lead else 'DIFFER'} {ca[:keep]}; "
                   f"figures of the old row {na}; missing from the new row: {missing or 'none'}; "
                   f"new figures {sorted(set(nb) - set(na))}")
    return res


out = [f"page {PAGE}: {OLD} against {NEW}"]
to, tn = tables(show(OLD, PAGE)), tables(show(NEW, PAGE))
out.append(f"tables: {len(to)} at the old revision, {len(tn)} at the new")
assert len(to) == len(tn)
changed = 0
for i, ((lo, a), (ln, b)) in enumerate(zip(to, tn), 1):
    same = h(a) == h(b)
    changed += not same
    out.append(f"table {i:2d} (line {lo} -> {ln}, {len(a)} lines, header {cells(a[0])[:3]}...): "
               f"{'byte-identical' if same else 'CHANGED'} sha256 {h(a)[:16]}" + ("" if same else f" -> {h(b)[:16]}"))
    if not same:
        assert len(a) == len(b), "row count changed"
        out += compare_rows(a, b, 2)
out.append(f"{len(to) - changed} of {len(to)} tables byte-identical; {changed} changed")
io, inn = show(OLD, INDEX).split("\n"), show(NEW, INDEX).split("\n")
rows = [(x, y) for x, y in zip(io, inn) if x != y]
out.append(f"index {INDEX}: {len(rows)} line(s) changed")
for x, y in rows:
    out += compare_rows([x], [y], 2)
print("\n".join(out))

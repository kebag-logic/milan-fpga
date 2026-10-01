#!/usr/bin/env python3
"""Prove which Markdown tables changed between two revisions of a page.

usage: table_proof.py <old_file> <new_file>

A table is a run of consecutive lines starting with '|'. Tables are matched in
order (the page's table count must not change). For each table it prints the
first source line in both revisions, the row count, the SHA-256 of the table's
bytes in each revision, and IDENTICAL or the unified diff of the rows.
"""
import difflib
import hashlib
import sys


def tables(path):
    out, cur, start = [], [], None
    for i, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
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


def main():
    old, new = tables(sys.argv[1]), tables(sys.argv[2])
    print(f"tables: old {len(old)}, new {len(new)}")
    assert len(old) == len(new), "table count changed"
    changed = 0
    for k, ((so, to), (sn, tn)) in enumerate(zip(old, new), 1):
        ho = hashlib.sha256("\n".join(to).encode()).hexdigest()
        hn = hashlib.sha256("\n".join(tn).encode()).hexdigest()
        same = to == tn
        changed += not same
        print(f"table {k}: old line {so}, new line {sn}, rows {len(to)}/{len(tn)}, "
              f"sha256 {ho[:16]}/{hn[:16]}, {'IDENTICAL' if same else 'CHANGED'}")
        if not same:
            for d in difflib.unified_diff(to, tn, lineterm="", n=0):
                if not d.startswith(("---", "+++")):
                    print("  " + d)
    print(f"changed tables: {changed}")


if __name__ == "__main__":
    main()

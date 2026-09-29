#!/usr/bin/env python3
"""Prove the round-2 edit left every measurement table byte-identical.

usage: table_identity.py <repo> <base-rev> <new-rev>

For both findings pages, every Markdown table (a run of lines starting with
"|") is read at the base and at the new revision with `git show`. Each base
table is looked up, as a byte-identical block of lines, in the new page.
The first table on each page is the verdict table; every other table is a
measurement, contract or hash table and must be unchanged. Tables that exist
only at the new revision are listed. A unified diff of the table lines alone
closes the report: it must show only verdict rows removed and added and the
new tables added.
"""
import difflib
import subprocess
import sys

PAGES = ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md")


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode("utf-8")


def tables(text):
    out, cur, start = [], [], 0
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


def main():
    repo, base, new = sys.argv[1:4]
    bad = 0
    for page in PAGES:
        a, b = show(repo, base, page), show(repo, new, page)
        ta, tb = tables(a), tables(b)
        blocks_b = ["\n".join(t) for _, t in tb]
        print(f"== {page}: {len(ta)} tables at {base}, {len(tb)} at {new}")
        for i, (line, t) in enumerate(ta):
            block = "\n".join(t)
            same = block in blocks_b
            role = "verdict" if i == 0 else "measurement/contract/hash"
            print(f"  base table {i + 1} at line {line}, {len(t)} lines, {role}, header {t[0][:60]!r}: "
                  f"{'BYTE-IDENTICAL' if same else 'CHANGED'}")
            if not same and i != 0:
                bad += 1
        blocks_a = ["\n".join(t) for _, t in ta]
        for line, t in tb:
            if "\n".join(t) not in blocks_a and t[0] != ta[0][1][0]:
                print(f"  new table at line {line}, {len(t)} lines, header {t[0][:60]!r}")
        la = [x for _, t in ta for x in t]
        lb = [x for _, t in tb for x in t]
        diff = list(difflib.unified_diff(la, lb, f"{base}:{page} (table lines)", f"{new}:{page} (table lines)",
                                         n=0, lineterm=""))
        print("  table-line diff:")
        for d in diff:
            print("    " + (d if len(d) < 160 else d[:157] + "..."))
    print(f"RESULT measurement/contract/hash tables changed: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

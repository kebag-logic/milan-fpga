#!/usr/bin/env python3
"""Round-2 table identity check.

Usage: tables_r2.py <clone> <old-rev> <new-rev> <pr-body-now.md>

For both findings pages, extracts every Markdown table (a run of lines that
start with '|') at the old and new revision, keyed by the nearest preceding
heading and its header row, and reports which tables are byte-identical,
changed, removed or added. For every changed table, the removed and added
lines are printed. Also compares every table in the current PR body with the
same-header table on the #606 / #608 page at the new revision.
"""
import subprocess
import sys

clone, old, new, body = sys.argv[1:5]
PAGES = ["docs/findings/606_FIRST_BIND_MEASUREMENT.md", "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md"]


def show(rev, path):
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout.decode()


def tables(text):
    out, head, cur = [], "(top)", []
    for line in text.split("\n") + [""]:
        if line.startswith("|"):
            cur.append(line)
            continue
        if cur:
            out.append(((head, cur[0]), cur))
            cur = []
        if line.startswith("#"):
            head = line
    return out


ok = True
for p in PAGES:
    a, b = tables(show(old, p)), tables(show(new, p))
    da, db = dict(a), dict(b)
    print(f"== {p}: {len(a)} tables at old, {len(b)} at new")
    for key, rows in a:
        if key not in db:
            print(f"  REMOVED/RE-HEADED  {key[0]} | {key[1][:60]}")
        elif db[key] == rows:
            print(f"  IDENTICAL {len(rows):4d} lines  {key[0]} | {key[1][:60]}")
        else:
            print(f"  CHANGED   {key[0]} | {key[1][:60]}")
            for r in rows:
                if r not in db[key]:
                    print("     - " + r[:200])
            for r in db[key]:
                if r not in rows:
                    print("     + " + r[:200])
    for key, rows in b:
        if key not in da:
            print(f"  ADDED     {len(rows):4d} lines  {key[0]} | {key[1][:60]}")
    # line-level: every table line at old that is absent at new
    la = [r for _k, rs in a for r in rs]
    lb = set(r for _k, rs in b for r in rs)
    gone = [r for r in la if r not in lb]
    print(f"  table lines at old absent at new: {len(gone)}")
    for r in gone:
        print("     x " + r[:160])

print("== PR body tables against the pages at", new)
page_tables = {}
for p in PAGES:
    for key, rows in tables(show(new, p)):
        page_tables.setdefault(key[1], []).append((p, rows))
for key, rows in tables(open(body).read().replace("\r\n", "\n")):
    cands = page_tables.get(key[1], [])
    same = [p for p, r in cands if r == rows]
    print(f"  {len(rows):4d} lines  {key[0]} | {key[1][:60]}  -> identical on: {same or 'NO PAGE TABLE'}")

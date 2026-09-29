#!/usr/bin/env python3
"""Compare every Markdown table line of the two B1 pages between two commits.

usage: table_diff.py <repo> <old-rev> <new-rev>
Groups consecutive '|' lines into tables keyed by the nearest preceding heading
and the header row, then reports tables unchanged, changed (with the changed
rows), added and removed. Exit 0 always; the report is the result.
"""
import subprocess
import sys

repo, old, new = sys.argv[1:4]
PAGES = ["docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md"]


def tables(rev, page):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], check=True,
                          capture_output=True).stdout.decode()
    out, cur, head = [], None, ""
    for line in text.splitlines():
        if line.startswith("#"):
            head = line
        if line.startswith("|"):
            if cur is None:
                cur = {"head": head, "rows": []}
                out.append(cur)
            cur["rows"].append(line)
        else:
            cur = None
    return out


for page in PAGES:
    a, b = tables(old, page), tables(new, page)
    ka = {(t["head"], t["rows"][0]): t["rows"] for t in a}
    kb = {(t["head"], t["rows"][0]): t["rows"] for t in b}
    print(f"== {page}: {len(a)} tables at old, {len(b)} at new")
    for k, rows in ka.items():
        if k not in kb:
            print(f"  REMOVED table under {k[0]!r}")
        elif kb[k] == rows:
            print(f"  identical ({len(rows)} lines) under {k[0]!r}: {k[1][:60]!r}")
        else:
            ch = [(i, r, kb[k][i] if i < len(kb[k]) else None) for i, r in enumerate(rows) if i >= len(kb[k]) or kb[k][i] != r]
            print(f"  CHANGED under {k[0]!r}: {len(ch)} row(s) differ; old {len(rows)} lines, new {len(kb[k])}")
            for i, r, s in ch:
                print(f"    row {i} old: {r[:150]}")
                print(f"    row {i} new: {(s or '')[:150]}")
    for k, rows in kb.items():
        if k not in ka:
            print(f"  ADDED table under {k[0]!r} ({len(rows)} lines): {k[1][:80]!r}")

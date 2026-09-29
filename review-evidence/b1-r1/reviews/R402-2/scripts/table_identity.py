#!/usr/bin/env python3
"""Compare every Markdown table block of the two B1 findings pages between two commits.

usage: table_identity.py <repo> <old-rev> <new-rev>
Prints, per page, each table (identified by its header line) as IDENTICAL,
CHANGED (with a line diff), ADDED or REMOVED. Exit 0 always; the receipt is read.
"""
import difflib
import subprocess
import sys

PAGES = ("docs/findings/599_394_E1_LINK_CYCLES.md", "docs/findings/387_SOFTWARE_GM_STEP.md")


def tables(repo, rev, page):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"], check=True,
                          capture_output=True, text=True).stdout
    out, cur = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            cur.append(line)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def main():
    repo, old, new = sys.argv[1:4]
    for page in PAGES:
        a, b = tables(repo, old, page), tables(repo, new, page)
        print(f"== {page}: {len(a)} tables at {old[:8]}, {len(b)} at {new[:8]}")
        amap = {t[0]: t for t in a}
        bmap = {t[0]: t for t in b}
        seen = set()
        for t in b:
            h = t[0]
            if h in seen:
                print("  DUPLICATE HEADER", h[:80])
            seen.add(h)
            if h not in amap:
                print(f"  ADDED     ({len(t)} lines) {h[:100]}")
            elif amap[h] == t:
                print(f"  IDENTICAL ({len(t)} lines) {h[:100]}")
            else:
                print(f"  CHANGED   ({len(t)} lines) {h[:100]}")
                for d in difflib.unified_diff(amap[h], t, lineterm="", n=0):
                    print("    " + d[:300])
        for t in a:
            if t[0] not in bmap:
                print(f"  REMOVED   ({len(t)} lines) {t[0][:100]}")


if __name__ == "__main__":
    main()

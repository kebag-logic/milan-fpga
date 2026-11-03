#!/usr/bin/env python3
"""For every 'path lines A-B' citation in scripts/docs_inventory.json of a file
that changed between two commits, report whether the cited block is still at
the same lines at the newer commit, and where it is verbatim if it moved.
Usage (run with -I from the repository root):
  python3 -I cited_line_shift.py <old-commit> <new-commit> <path>...
"""
import json, re, subprocess, sys

old_rev, new_rev, files = sys.argv[1], sys.argv[2], sys.argv[3:]
data = json.dumps(json.load(open("scripts/docs_inventory.json")))


def show(rev, path):
    out = subprocess.run(["git", "show", f"{rev}:{path}"],
                         capture_output=True, text=True).stdout
    return out.split("\n")


seen = set()
for path in files:
    old, new = show(old_rev, path), show(new_rev, path)
    pat = re.escape(path) + r"`?\s*(?:lines?|:)\s*(\d+)(?:\s*[-–]\s*(\d+))?"
    for m in re.finditer(pat, data):
        a = int(m.group(1)); b = int(m.group(2) or a)
        if (path, a, b) in seen:
            continue
        seen.add((path, a, b))
        blk = old[a - 1:b]
        hits = [i + 1 for i in range(len(new) - len(blk) + 1)
                if new[i:i + len(blk)] == blk]
        where = ",".join(f"{h}-{h + len(blk) - 1}" for h in hits) or "NOT FOUND"
        print(f"{path}:{a}-{b} same_lines={new[a - 1:b] == blk} verbatim_at={where}")

#!/usr/bin/env python3
"""Census of a published evidence tree against its own INDEX.md files.

evidence_census.py LISTING DLROOT PREFIX
LISTING: lines "<type> <size> <path>" from the git tree API (recursive).
DLROOT:  directory holding the downloaded INDEX.md files under their paths.
For every INDEX.md present, each file row and each linked sub-directory it
names is looked up in LISTING; anything named but absent is printed MISSING.
Exit 1 if anything is missing.
"""
import re, sys
from pathlib import Path

listing, dlroot, prefix = sys.argv[1:4]
present = {}
for line in open(listing):
    t, size, path = line.rstrip("\n").split(" ", 2)
    present[path] = (t, size)

missing = 0
named = 0
for idx in sorted(Path(dlroot).rglob("INDEX.md")):
    rel = idx.relative_to(dlroot).as_posix()
    d = rel.rsplit("/", 1)[0]
    text = idx.read_text()
    for sub in re.findall(r"\[`([^`]+)/`\]", text):
        named += 1
        if f"{d}/{sub}" not in present:
            print(f"MISSING dir  {d}/{sub}/ (named by {rel})"); missing += 1
    for name, size in re.findall(r"^\| `([^`]+)` \| (\d+) \|", text, re.M):
        named += 1
        p = f"{d}/{name}"
        if p not in present:
            print(f"MISSING file {p} ({size} B, named by {rel})"); missing += 1
        elif present[p][1] != size:
            print(f"SIZE  {p}: index {size}, tree {present[p][1]}")
print(f"{named} entries named by INDEX files, {missing} missing from the tree")
sys.exit(1 if missing else 0)

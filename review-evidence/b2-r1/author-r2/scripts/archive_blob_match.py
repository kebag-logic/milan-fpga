#!/usr/bin/env python3
"""Check the console and MSRP inputs against the archive commit's git tree.

usage: archive_blob_match.py <round-1 packet author dir> <tree JSON>

The tree JSON is `gh api repos/kebag-logic/milan-fpga/git/trees/<archive commit>?recursive=1`
for archive commit 666d8897bc0659b7d2d29ef222437da5087d586e. Every console*.txt
and msrp.tsv under the author dir is hashed with `git hash-object` and compared
with the tree's blob id at review-evidence/b2-r1/author/<same path>. Exit 0 only
when all match, so the values the round-2 scripts derive come from the archived
bytes.
"""
import json
import subprocess
import sys
from pathlib import Path

A = Path(sys.argv[1])
tree = json.load(open(sys.argv[2]))
blobs = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "blob"}
files = sorted(A.rglob("console*.txt")) + sorted(A.rglob("msrp.tsv"))
bad = []
for f in files:
    h = subprocess.run(["git", "hash-object", str(f)], capture_output=True, text=True, check=True).stdout.strip()
    if blobs.get("review-evidence/b2-r1/author/" + f.relative_to(A).as_posix()) != h:
        bad.append(f.relative_to(A).as_posix())
print(f"tree truncated: {tree['truncated']}; files checked: {len(files)} "
      f"({sum(p.name.startswith('console') for p in files)} console, {sum(p.name == 'msrp.tsv' for p in files)} msrp.tsv)")
print(f"git blob equal to the archive tree: {len(files) - len(bad)}; different: {len(bad)} {bad or ''}")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Check that a merge keeps both sides' changes, line by line, and recount the audit from the blobs.

Usage: merge_sides.py <repo> <base> <ours> <theirs> <merge> <head>
"""
import difflib
import re
import subprocess
import sys

repo, base, ours, theirs, merge, head = sys.argv[1:7]


def git(*args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def lines(rev, path):
    return git("show", f"{rev}:{path}").decode("utf-8").split("\n")


def delta(old, new):
    added, removed = [], []
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            removed += old[i1:i2]
            added += new[j1:j2]
    return added, removed


failed = 0
path = "docs/testing/TESTING.md"
b, o, t, m = (lines(r, path) for r in (base, ours, theirs, merge))
kept = set(m)
for name, side in (("PR side", o), ("dev side", t)):
    added, removed = delta(b, side)
    lost = [x for x in added if x not in kept]
    back = [x for x in removed if x in kept and x not in set(o if side is t else t)]
    print(f"{path} {name}: +{len(added)} -{len(removed)} lost={len(lost)} removed-but-present={len(back)}")
    for x in lost + back:
        print("   ", x[:200])
    failed += len(lost) + len(back)

# Every merged line comes from one side: the auto-merge invented nothing.
invented = [x for x in m if x not in set(o) and x not in set(t)]
print(f"{path} merged lines on neither parent: {len(invented)}")
failed += len(invented)

# A line count for every page row, against the head's own blobs.
audit = git("show", f"{head}:docs/DOCUMENTATION_AUDIT.md").decode("utf-8")
row = re.compile(r"^\| \[([^\]]+?)(?: \(historical\))?\]\([^)]*\) \| (\d+) \| ", re.M)
tracked = [p for p in git("ls-tree", "-r", "--name-only", head).decode().splitlines()]
seen = {}
for page, count in row.findall(audit):
    if page in tracked and page not in seen:
        seen[page] = int(count)
mismatch = 0
total = 0
for page, count in sorted(seen.items()):
    data = git("show", f"{head}:{page}").decode("utf-8", "replace")
    real = len(data.splitlines())
    total += real
    if real != count:
        mismatch += 1
        print(f"line count differs: {page} audit={count} blob={real}")
print(f"page rows {len(seen)} line-count mismatches {mismatch} recounted total {total:,}")
failed += mismatch

summary = re.search(r"\*\*total\*\* \| \*\*(\d+)\*\* \| \*\*([\d,]+)\*\*", audit)
print("audit summary total:", summary.group(1), summary.group(2))
if int(summary.group(1)) != len(seen) or summary.group(2) != f"{total:,}":
    print("summary total differs from recount")
    failed += 1

print("RESULT", "FAIL" if failed else "PASS", failed)
sys.exit(1 if failed else 0)

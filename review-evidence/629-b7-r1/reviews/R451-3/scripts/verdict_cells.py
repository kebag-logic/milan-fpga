#!/usr/bin/env python3
"""Compare the verdict/judgement column of every table row in the page's lane B7 section
across commits. Rows are keyed by their first cell; the second cell is the verdict or judgement.
Usage: verdict_cells.py <repo> <commit> [<commit> ...]
"""
import subprocess
import sys

repo, commits = sys.argv[1], sys.argv[2:]
PAGE = "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"


def cells(c):
    t = subprocess.run(["git", "-C", repo, "show", f"{c}:{PAGE}"], check=True, capture_output=True, text=True).stdout
    lines = t.split("\n")
    s = lines.index("## Dev bbf704ec, 2026-10-03: lane B7")
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    out = {}
    for l in lines[s:e]:
        if l.startswith("| ") and not l.startswith("|---"):
            parts = [p.strip() for p in l.strip().strip("|").split(" | ")]
            if len(parts) >= 2:
                out.setdefault(parts[0], parts[1])
    return out


base = cells(commits[0])
print(f"{commits[0][:8]}: {len(base)} keyed rows")
diffs = 0
for c in commits[1:]:
    cur = cells(c)
    added = sorted(set(cur) - set(base))
    removed = sorted(set(base) - set(cur))
    changed = sorted(k for k in set(cur) & set(base) if cur[k] != base[k])
    print(f"{c[:8]}: {len(cur)} keyed rows; first-cell keys added={len(added)} removed={len(removed)} second-cell changed={len(changed)}")
    for k in changed:
        print(f"  CHANGED {k[:70]!r}: {base[k][:80]!r} -> {cur[k][:80]!r}")
    diffs += len(changed) + len(added) + len(removed)
verd = cells(commits[-1])
for k in ("A0, the peer on INTERNAL", ):
    pass
print("verdict-like cells at last commit:")
for k, v in verd.items():
    if any(w in v for w in ("PASS", "FAIL", "NOT RUN", "Met", "Observed", "Not met")):
        print(f"  {k[:60]!r}: {v[:70]!r}")
print("RESULT", "unchanged" if diffs == 0 else f"{diffs} differences")

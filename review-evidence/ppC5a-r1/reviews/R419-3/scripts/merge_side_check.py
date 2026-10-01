#!/usr/bin/env python3
"""Compare what one merge side changed against what the merge carried.

For a merge M = merge(L, R) with base B, the R side's change is diff(B, R).
Applied to L, the merge should carry diff(L, M) with the same added and
removed lines, except where a conflict resolution edited them. This prints,
per file, the multiset difference of added and removed lines between the
two diffs: lines R added that M did not carry (LOST), and lines M carries
that R did not add (EXTRA, i.e. resolution edits). Usage:
  merge_side_check.py REPO BASE SIDE OTHER MERGE
"""
import collections, subprocess, sys

def diff_lines(repo, a, b):
    out = subprocess.run(["git", "-C", repo, "diff", "--no-color", "-U0",
                          "--no-renames", a, b], check=True,
                         capture_output=True, text=True,
                         errors="surrogateescape").stdout
    per = collections.defaultdict(lambda: (collections.Counter(),
                                           collections.Counter()))
    cur = None
    for ln in out.splitlines():
        if ln.startswith("diff --git "):
            cur = ln.split(" b/", 1)[1]
        elif ln.startswith("+++") or ln.startswith("---"):
            continue
        elif ln.startswith("+") and cur:
            per[cur][0][ln[1:]] += 1
        elif ln.startswith("-") and cur:
            per[cur][1][ln[1:]] += 1
    return per

repo, base, side, other, merge = sys.argv[1:6]
want = diff_lines(repo, base, side)     # what the side changed
got = diff_lines(repo, other, merge)    # what the merge brought to the other
total_lost = 0
for f in sorted(set(want) | set(got)):
    wa, wr = want[f]
    ga, gr = got[f]
    lost_a = wa - ga
    extra_a = ga - wa
    lost_r = wr - gr
    if lost_a or extra_a or lost_r:
        print(f"== {f}")
        for l, n in lost_a.items():
            print(f"  LOST+ x{n}: {l[:150]}")
        for l, n in lost_r.items():
            print(f"  NOTREMOVED- x{n}: {l[:150]}")
        for l, n in extra_a.items():
            print(f"  EXTRA+ x{n}: {l[:150]}")
        total_lost += sum(lost_a.values())
print(f"files compared: {len(set(want) | set(got))}; side-added lines not carried: {total_lost}")

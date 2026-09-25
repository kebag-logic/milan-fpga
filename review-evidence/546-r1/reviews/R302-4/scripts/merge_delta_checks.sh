#!/bin/sh
# Merge-delta proofs for PR #554 round 4. Run from a clone that has all four commits.
# Usage: merge_delta_checks.sh <out-dir>
set -eu
OUT=$1; mkdir -p "$OUT"
BASE=57456af96b3127b9d309a995bbbd35a6113ce52d   # PR's original source base
R3=0c61d458941088f3847513b7c6fe6589c75b4270     # reviewed round-3 head (parent 1)
DEV=c266432dcb0cdd464205823a3d82cad260eedde2    # dev merged in (parent 2)
M=f5532c4c3f94a516b748cc4627dc5f78d05fa73e      # merge head under review
[ "$(git rev-parse $M^1) $(git rev-parse $M^2)" = "$R3 $DEV" ] && echo "parents OK" > "$OUT/parents.txt"
[ "$(git merge-base $R3 $DEV)" = "$BASE" ] && echo "merge-base = $BASE" >> "$OUT/parents.txt"
chg() { git -c core.pager=cat diff --no-ext-diff --no-color "$1" "$2" | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' || true; }
# 1. the PR's own change against new dev equals the reviewed change against the old base, line for line
chg $BASE $R3 > "$OUT/pr_changed_lines_old_base.txt"; chg $DEV $M > "$OUT/pr_changed_lines_new_dev.txt"
cmp "$OUT/pr_changed_lines_old_base.txt" "$OUT/pr_changed_lines_new_dev.txt" && echo "PR changed lines identical" >> "$OUT/parents.txt"
# 2. the merge adds nothing beyond dev on the author side
chg $BASE $DEV > "$OUT/dev_changed_lines.txt"; chg $R3 $M > "$OUT/merge_minus_r3_changed_lines.txt"
cmp "$OUT/dev_changed_lines.txt" "$OUT/merge_minus_r3_changed_lines.txt" && echo "dev-side changed lines identical" >> "$OUT/parents.txt"
# 3. same file sets
git diff --name-only $BASE $R3 > "$OUT/pr_files_old.txt"; git diff --name-only $DEV $M > "$OUT/pr_files_new.txt"
cmp "$OUT/pr_files_old.txt" "$OUT/pr_files_new.txt" && echo "PR file set identical (22 files)" >> "$OUT/parents.txt"
# 4. manual resolutions only where git conflicted
git -c core.pager=cat show --no-color --remerge-diff --format=%H $M > "$OUT/remerge_diff.txt"
grep '^diff --git' "$OUT/remerge_diff.txt" >> "$OUT/parents.txt"
cat "$OUT/parents.txt"

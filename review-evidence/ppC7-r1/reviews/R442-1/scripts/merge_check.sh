#!/usr/bin/env bash
# Recompute merge e2c7d97 = 751e1c0 (lane) + c74711d (main): the two READMEs
# both sides touched, by git merge-file, and every other file from its side.
# Usage: merge_check.sh <clone> <scratchdir>
set -uo pipefail
C=$1; S=$2; mkdir -p "$S"; cd "$C" || exit 1
M=e2c7d97d158a30e44289a06a33f8ff4c5e289b87; L=751e1c0a940d9fe9c242caa9f2233d451b29c447; T=c74711d45a8bbc0d6b38cb49211b26a4a6413e88
B=$(git merge-base $L $T); echo "merge-base $B"; echo "parents $(git rev-parse $M^1) $(git rev-parse $M^2)"
for f in tb/adp_engine/README.md tb/pp_top/README.md; do
  n=$(echo "$f" | tr / _)
  git show $L:"$f" >"$S/$n.ours"; git show $B:"$f" >"$S/$n.base"; git show $T:"$f" >"$S/$n.theirs"
  git merge-file -p "$S/$n.ours" "$S/$n.base" "$S/$n.theirs" >"$S/$n.merged"; echo "$f merge-file conflicts=$?"
  if git show $M:"$f" | cmp -s - "$S/$n.merged"; then echo "$f IDENTICAL to the merge"; else echo "$f DIFFERS"; fi
done
git diff --name-only $B $T | sort >"$S/main_side"; git diff --name-only $B $L | sort >"$S/lane_side"
echo "both sides: $(comm -12 "$S/main_side" "$S/lane_side" | tr '\n' ' ')"
bad=0
for f in $(comm -23 "$S/main_side" "$S/lane_side"); do [ "$(git rev-parse $T:"$f" 2>/dev/null)" = "$(git rev-parse $M:"$f" 2>/dev/null)" ] || { echo "main-only file differs: $f"; bad=1; }; done
for f in $(comm -13 "$S/main_side" "$S/lane_side"); do [ "$(git rev-parse $L:"$f" 2>/dev/null)" = "$(git rev-parse $M:"$f" 2>/dev/null)" ] || { echo "lane-only file differs: $f"; bad=1; }; done
echo "main-only files: $(comm -23 "$S/main_side" "$S/lane_side" | wc -l), lane-only files: $(comm -13 "$S/main_side" "$S/lane_side" | wc -l), mismatches: $bad"

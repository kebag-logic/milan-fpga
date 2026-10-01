#!/bin/sh
# Re-derive merge a8fe574 of PR #138: for every file both sides changed since
# the merge base, run git merge-file (lane = first parent, main = second) and
# compare with the published merge; for conflicted files, check that each
# side's lines survive in order (check_merge_sides.py).
# Usage: reconstruct_merge.sh REPO WORKDIR
set -eu
REPO=$1; W=$2; HERE=$(cd "$(dirname "$0")" && pwd)
X=a8fe57448bbaa8dabc7e842600aa4f10e04336e3
L=$(git -C "$REPO" rev-parse "$X^1"); M=$(git -C "$REPO" rev-parse "$X^2")
B=$(git -C "$REPO" merge-base "$L" "$M")
echo "merge $X parents lane $L main $M base $B"
mkdir -p "$W"
comm -12 <(git -C "$REPO" diff --name-only "$B" "$M" | sort) \
         <(git -C "$REPO" diff --name-only "$B" "$L" | sort) > "$W/both.txt" 2>/dev/null || true
for f in $(cat "$W/both.txt"); do
  n=$(echo "$f" | tr / _)
  git -C "$REPO" show "$L:$f" > "$W/$n.auto"; git -C "$REPO" show "$B:$f" > "$W/$n.base"
  git -C "$REPO" show "$M:$f" > "$W/$n.main"; git -C "$REPO" show "$X:$f" > "$W/$n.merged"
  set +e; git merge-file -L lane -L base -L main "$W/$n.auto" "$W/$n.base" "$W/$n.main"; c=$?; set -e
  if [ "$c" = 0 ]; then
    cmp -s "$W/$n.auto" "$W/$n.merged" && echo "$f: clean automatic merge, equal to the published merge" \
      || echo "$f: clean automatic merge, DIFFERS from the published merge"
  else
    echo "## $f: $c conflict region(s)"; python3 "$HERE/check_merge_sides.py" "$W/$n.auto" "$W/$n.merged"
  fi
done
for side in main lane; do
  if [ $side = main ]; then S=$M; O=$L; else S=$L; O=$M; fi
  n=0; d=0
  for f in $(comm -23 <(git -C "$REPO" diff --name-only "$B" "$S" | sort) <(git -C "$REPO" diff --name-only "$B" "$O" | sort)); do
    n=$((n+1)); [ "$(git -C "$REPO" rev-parse "$S:$f" 2>/dev/null)" = "$(git -C "$REPO" rev-parse "$X:$f" 2>/dev/null)" ] || { d=$((d+1)); echo "DIFF $f"; }
  done
  echo "$side-only files: $n, differing from that side at the merge: $d"
done

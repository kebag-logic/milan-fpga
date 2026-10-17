#!/usr/bin/env bash
# For each path the candidate changes relative to either parent, report whether
# its candidate blob equals the other parent's blob (i.e. it was taken whole).
# usage: composition_check.sh <candidate> <dev-parent> <pr-head>
set -eu
C=$1 D=$2 H=$3
echo "candidate vs pr-head (dev-side paths):"
git diff --name-only "$H" "$C" | while read -r p; do
  c=$(git rev-parse "$C:$p" 2>/dev/null || echo none); d=$(git rev-parse "$D:$p" 2>/dev/null || echo none)
  [ "$c" = "$d" ] && echo "  taken-from-dev $p" || echo "  MERGED $p"
done
echo "candidate vs dev (pr-side paths):"
git diff --name-only "$D" "$C" | while read -r p; do
  c=$(git rev-parse "$C:$p" 2>/dev/null || echo none); h=$(git rev-parse "$H:$p" 2>/dev/null || echo none)
  [ "$c" = "$h" ] && echo "  taken-from-pr $p" || echo "  MERGED $p"
done

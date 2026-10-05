#!/bin/bash
# usage: mkpoint.sh <commit> <name>  -> detached worktree $VALIDATION_STORAGE/656-a536/pts/<name>,
# submodules as shared clones checked out at that commit's gitlinks
set -euo pipefail
LANE=$LANES/656-dp-gptp-order
c=$(git -C "$LANE" rev-parse "$1^{commit}")
d=$VALIDATION_STORAGE/656-a536/pts/$2
if [ -e "$d" ]; then git -C "$LANE" worktree remove --force "$d" 2>/dev/null || rm -rf "$d"; fi
git -C "$LANE" worktree prune
git -C "$LANE" worktree add --detach "$d" "$c" >/dev/null 2>&1
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  top=$(git -C "$LANE/$sm" rev-parse --show-toplevel)
  [ "$top" = "$LANE/$sm" ] || { echo "bad toplevel $top for $sm" >&2; exit 3; }
  s=$(git -C "$LANE" ls-tree "$c" "$sm" | awk '{print $3}')
  rm -rf "$d/$sm"
  git clone --quiet --shared --no-checkout "$LANE/$sm" "$d/$sm"
  top2=$(git -C "$d/$sm" rev-parse --show-toplevel)
  [ "$top2" = "$d/$sm" ] || { echo "bad clone toplevel $top2" >&2; exit 4; }
  git -C "$d/$sm" checkout --quiet --detach "$s"
  echo "$sm $s $(git -C "$d/$sm" rev-parse HEAD)"
done
echo "point $2 = $c $(git -C "$d" rev-parse HEAD)"

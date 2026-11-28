#!/usr/bin/env bash
# Verify a base-merge commit of a PR lane: parents, tree, recomputed merge, submodule
# containment, and the content delta. Read-only on the repository (uses a throwaway
# index file under $TMPDIR for the reverse-apply check).
# Usage: verify_base_merge.sh <repo> <head> <lane-parent> <base-tip> <old-base> <gitlink-path>
set -u
repo=$1 H=$2 A=$3 D=$4 OLD=$5 SUB=$6
g() { git -C "$repo" "$@"; }
fail=0
echo "# verify_base_merge head=$H lane-parent=$A base-tip=$D old-base=$OLD submodule=$SUB"
echo "## (1) parents"
parents=$(g rev-list --parents -n1 "$H" | cut -d' ' -f2-)
echo "parents: $parents"
[ "$parents" = "$A $D" ] && echo "(1) PASS parents are exactly [lane-parent, base-tip]" || { echo "(1) FAIL"; fail=1; }
echo "## (2) trees"
tH=$(g rev-parse "$H^{tree}"); tA=$(g rev-parse "$A^{tree}"); tD=$(g rev-parse "$D^{tree}")
echo "tree head=$tH lane-parent=$tA base-tip=$tD"
mt=$(g merge-tree --write-tree "$A" "$D"); mrc=$?
echo "merge-tree --write-tree lane-parent base-tip: rc=$mrc tree=$(echo "$mt" | head -1)"
[ $mrc -eq 0 ] && [ "$(echo "$mt" | head -1)" = "$tH" ] && echo "(2) PASS head tree is the clean recomputed merge" || { echo "(2) FAIL"; fail=1; }
echo "merge-bases(lane-parent, base-tip): $(g merge-base --all "$A" "$D" | tr '\n' ' ')"
for p in $(g rev-list --parents -n1 "$D" | cut -d' ' -f2-); do
  g merge-base --is-ancestor "$p" "$A" && echo "base-tip parent $p is an ancestor of lane-parent" || echo "base-tip parent $p is NOT an ancestor of lane-parent"
done
dp=($(g rev-list --parents -n1 "$D" | cut -d' ' -f2-))
if [ ${#dp[@]} -eq 2 ]; then
  rt=$(g merge-tree --write-tree "${dp[0]}" "${dp[1]}" | head -1)
  echo "base-tip recomputed from its parents: $rt (base-tip tree $tD) $( [ "$rt" = "$tD" ] && echo 'no content beyond its parents' || echo 'EVIL MERGE CONTENT')"
fi
echo "## (3) submodule gitlink"
lH=$(g ls-tree "$H" "$SUB" | awk '{print $3}'); lA=$(g ls-tree "$A" "$SUB" | awk '{print $3}'); lD=$(g ls-tree "$D" "$SUB" | awk '{print $3}')
echo "gitlink head=$lH lane-parent=$lA base-tip=$lD"
if git -C "$repo/$SUB" cat-file -e "$lD^{commit}" 2>/dev/null && git -C "$repo/$SUB" merge-base --is-ancestor "$lD" "$lH"; then
  echo "(3) PASS head gitlink contains base-tip's gitlink ($(git -C "$repo/$SUB" rev-list --count "$lD..$lH") commits past it)"
else echo "(3) FAIL"; fail=1; fi
echo "## (4) delta"
n=$(g diff "$A" "$H" | wc -c)
echo "diff lane-parent..head bytes: $n"
echo "files the base-tip's delta touches (old-base..base-tip): $(g diff --name-only "$OLD" "$D" | wc -l)"
if [ "$n" -eq 0 ]; then
  echo "(4) the merge changes no byte of the lane; the base's delta must already be in the lane:"
  g diff --name-only "$OLD" "$D" | while read -r f; do
    [ "$(g rev-parse "$H:$f")" = "$(g rev-parse "$D:$f")" ] && echo "  SAME-AS-BASE $f" || echo "  LANE-DIFFERS $f (last lane commit: $(g log -1 --format='%h' "$OLD..$H" -- "$f"))"
  done
fi
exit $fail

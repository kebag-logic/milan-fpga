#!/usr/bin/env bash
# Apply the four supplied adaptation patches, in the assigned order, to the gitlink commit's tree in a
# private index (no work-tree or ref change) and compare each cumulative tree with the committed one.
# Usage: patch_equivalence.sh <repo> <patch-dir>
set -eu
repo=$1; pd=$2; idx=$(mktemp); trap 'rm -f "$idx"' EXIT
cd "$repo"
export GIT_INDEX_FILE=$idx
git read-tree 4a2f8ae418a324a7476c4cb2d3fbc0813345e273
rc=0
for pair in c8-bbf704ec:dbd9e246728e641984f5601a4cbcae4acfb60d25 p2-p1-1269cdaf:eefffe50f46e4d5bbf2255bb044789285ef24808 \
            c10-1269cdaf:880a40fc6d33e68b76d6ef9eceb7e9b5f7caa9e1 232-241f9184:42c63ebc99fa4d3808a054b140d1b0167dd3bc9c; do
  p=${pair%%:*}; c=${pair#*:}
  git apply --cached "$pd/parent-adoption-$p.patch"
  got=$(git write-tree); want=$(git rev-parse "$c^{tree}")
  if [ "$got" = "$want" ]; then echo "EQUAL $p -> $got (commit ${c:0:9})"; else echo "DIFFERENT $p applied=$got committed=$want"; rc=1; fi
done
sha256sum "$pd"/parent-adoption-*.patch | sed "s|$pd/||"
exit $rc

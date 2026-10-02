#!/bin/bash
# Build a scratch parent: mkparent.sh <dir> <dev|pr634> <processor-commit> [patch...]
# git archive of the parent tree, its gitlinks recorded, gptp-processor and
# verilog-axis cloned at their pins, protocol-processor a clone of the lane at
# <processor-commit> with its gitlink recorded, then each patch applied --index.
set -euo pipefail
dir=$1; which=$2; pp=$3; shift 3
S=$VALIDATION_STORAGE/c8-a504/src
LANE=$LANES/ppC8-desc-lint
case $which in
  dev) repo=$LANES/trusted-dev-20261002-cdf49d1a; rev=cdf49d1a28527562888f0a903de51b6b15b1244f ;;
  pr634) repo=$S/milan-fpga-pr634.git; rev=$(git -C $repo rev-parse pr634) ;;
esac
rm -rf "$dir"; mkdir -p "$dir"
git -C "$repo" archive "$rev" | tar -x -C "$dir"
cd "$dir"
git init -q
git -c user.name=scratch -c user.email=scratch@localhost add -A
while read -r mode type sha path; do
  git update-index --add --cacheinfo "160000,$sha,$path"
done < <(git -C "$repo" ls-tree -r "$rev" | awk '$2=="commit"')
git -c user.name=scratch -c user.email=scratch@localhost commit -q -m "parent $which $rev"
echo "tree $(git rev-parse HEAD^{tree}) parent $(git -C "$repo" rev-parse "$rev^{tree}")"
pin() { git -C "$repo" ls-tree "$rev" "$1" | awk '{print $3}'; }
rmdir gptp-processor third_party/verilog-axis protocol-processor 2>/dev/null || true
git clone -q "$S/gptp-processor.git" gptp-processor && git -C gptp-processor checkout -q "$(pin gptp-processor)"
git clone -q "$S/verilog-axis.git" third_party/verilog-axis && git -C third_party/verilog-axis checkout -q "$(pin third_party/verilog-axis)"
git clone -q "$LANE" protocol-processor && git -C protocol-processor checkout -q "$pp"
for p in "$@"; do git apply --index ${APPLY_OPTS:-} "$p"; echo "applied $(basename "$p") ${APPLY_OPTS:-}"; done
git update-index --cacheinfo "160000,$(git -C protocol-processor rev-parse HEAD),protocol-processor"
git submodule init -q
git -c user.name=scratch -c user.email=scratch@localhost commit -q -m "patches and the processor at $pp"
echo "pins: gptp $(git -C gptp-processor rev-parse HEAD) axis $(git -C third_party/verilog-axis rev-parse HEAD) pp $(git -C protocol-processor rev-parse HEAD)"
git diff --stat HEAD~1 | tail -1

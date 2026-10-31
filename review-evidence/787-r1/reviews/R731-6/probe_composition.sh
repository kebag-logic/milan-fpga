#!/usr/bin/env bash
# Reproduce the composition facts of the #787 merge-train candidate.
# usage: probe_composition.sh <milan-fpga clone with the commits below> <scratch dir>
# Needs: e5b8405d (live dev), 86a349d5 (PR head), 808e64e3 (candidate),
# 125ac680 (candidate parent), 8adf5c99 and 81f78a81 (the two merge bases).
set -u
repo=$1; scratch=$2
DEV=e5b8405db4c1f7cbdafb5df92b15b580142e0232
HEAD_SHA=86a349d5399d8abc40b819d09806fc8245682609
CAND=808e64e39c1007e463cf20de892e6dca73bfa2a6
PARENT=125ac68006d124dd149b9161539dfaa787166e62
cd "$repo" || exit 2
echo "trees: dev=$(git rev-parse $DEV^{tree}) parent=$(git rev-parse $PARENT^{tree})"
echo "trees: head=$(git rev-parse $HEAD_SHA^{tree}) candidate=$(git rev-parse $CAND^{tree})"
echo "merge-tree(dev, head) = $(git merge-tree --write-tree $DEV $HEAD_SHA)"
echo "merge bases (dev, head):"; git merge-base --all $DEV $HEAD_SHA
for b in $(git merge-base --all $DEV $HEAD_SHA); do
  echo "single-base merge on $b:"
  git merge-tree --write-tree --name-only --merge-base=$b $DEV $HEAD_SHA; echo "rc=$?"
done
# The act-path change classifier of rtl-fast.yml, run against each base.
step=$(dirname "$(readlink -f "$0")")/receipts/classify_step.sh
rm -rf "$scratch/clsprobe"; git clone -q --no-checkout "$repo" "$scratch/clsprobe"
cd "$scratch/clsprobe" && git -c advice.detachedHead=false checkout -q $HEAD_SHA
for base in $DEV 8adf5c990bad73e80852e9c1df95163792a0deb2; do
  git update-ref refs/remotes/origin/dev $base
  t=$scratch/rt-$base; rm -rf "$t"; mkdir -p "$t"; : > "$t/out"
  ( export EVENT_NAME=pull_request ACT=true PR_BASE_REF=dev PR_HEAD_SHA=$HEAD_SHA \
           RUNNER_TEMP=$t GITHUB_OUTPUT=$t/out
    bash "$step" ) > "$t/log" 2>&1
  echo "classifier with origin/dev=$base rc=$? output: $(cat "$t/out" | tr '\n' ' ')"
done

#!/usr/bin/env bash
# The milan_dp recipe derives the protocol-processor source list with
# `git ls-files`. Replace the scratch copy of each submodule with a local
# clone (read-only on the reviewed clone) checked out at the head's gitlink,
# and verify the checked-out tree equals the gitlink's tree.
set -eu
REPO=${REPO:-$REVIEWS/r301-2-545}
PKT=${PKT:-$REVIEWS/545-r301-2-packet}
HEAD=b94f53cc4e5dbfd9527ba666922a55804515165c
T="$PKT/scratch/tree"
for s in protocol-processor gptp-processor; do
  pin=$(git -C "$REPO" rev-parse "$HEAD:$s")
  rm -rf "$T/$s"
  git clone -q --no-checkout "$REPO/.git/modules/$s" "$T/$s"
  git -C "$T/$s" -c advice.detachedHead=false checkout -q "$pin"
  echo "$s pin=$pin checkout=$(git -C "$T/$s" rev-parse HEAD) dirty=$(git -C "$T/$s" status --porcelain | wc -l)"
done

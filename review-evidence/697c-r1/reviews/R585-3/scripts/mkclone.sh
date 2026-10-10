#!/usr/bin/env bash
# A disposable clone of the review checkout at a revision, its submodules cloned from the checkout's own
# initialised ones at the revision's gitlinks. Usage: mkclone.sh <checkout> <rev> <dest>
set -eu
SRC=$(cd "$1" && pwd); REV=$2; D=$3
rm -rf "$D"; git clone --quiet --no-checkout "$SRC" "$D"
git -C "$D" -c advice.detachedHead=false checkout --quiet "$REV"
for sub in gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack; do
  want=$(git -C "$D" ls-tree "$REV" "$sub" | awk '{print $3}')
  [ -n "$want" ] || continue
  rmdir "$D/$sub" 2>/dev/null || true
  git clone --quiet --no-checkout "$SRC/$sub" "$D/$sub"
  git -C "$D/$sub" -c advice.detachedHead=false checkout --quiet "$want"
  echo "$sub $(git -C "$D/$sub" rev-parse HEAD)"
done
echo "clone $(git -C "$D" rev-parse HEAD) status=$(git -C "$D" status --porcelain | wc -l)"

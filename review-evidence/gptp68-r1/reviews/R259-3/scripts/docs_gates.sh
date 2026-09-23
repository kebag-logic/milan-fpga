#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# The donor's contract and docs gates at the head, in a scratch export, plus an
# em-dash scan of every line the branch adds (base..head).
set -u
. "$(dirname "$0")/env.sh"
dir=$SCRATCH/docs-head
rm -rf "$dir"; mkdir -p "$dir"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$dir"
cd "$dir"
rc=0
echo "== make contract"; make contract || rc=1
echo "== make docs"; make docs || rc=1
echo "== em-dash (U+2014) and en-dash (U+2013) in lines added base..head"
n=$(git -C "$CLONE" diff "$BASE_SHA" "$HEAD_SHA" | grep '^+' | grep -v '^+++' | grep -c "$(printf '\342\200\224')" || true)
m=$(git -C "$CLONE" diff "$BASE_SHA" "$HEAD_SHA" | grep '^+' | grep -v '^+++' | grep -c "$(printf '\342\200\223')" || true)
echo "added lines with U+2014: $n; with U+2013: $m"
[ "$n" = 0 ] || rc=1
echo "== non-ASCII characters in lines added to docs/"
git -C "$CLONE" diff "$BASE_SHA" "$HEAD_SHA" -- docs | grep '^+' | grep -v '^+++' | grep -nP '[^\x00-\x7F]' || echo "none"
exit $rc

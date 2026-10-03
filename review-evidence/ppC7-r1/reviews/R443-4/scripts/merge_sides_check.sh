#!/usr/bin/env bash
# For every file both sides of the merge changed, compare the patch-id of
#   (merge-base -> lane tip) with (main -> merge)   : the lane's lines, kept
#   (merge-base -> main)     with (lane tip -> merge): main's lines, kept
# Usage: merge_sides_check.sh <repo> <merge> <lane-tip> <main>
set -u
cd "$1" || exit 2
M=$2; L=$3; B=$4
MB=$(git merge-base "$L" "$B")
echo "merge-base $MB"
comm -12 <(git diff --name-only "$MB" "$L" | sort) <(git diff --name-only "$MB" "$B" | sort) | while read -r f; do
  lane1=$(git diff "$MB" "$L" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  lane2=$(git diff "$B" "$M" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  main1=$(git diff "$MB" "$B" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  main2=$(git diff "$L" "$M" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  l=$([ "$lane1" = "$lane2" ] && echo SAME || echo DIFF); m=$([ "$main1" = "$main2" ] && echo SAME || echo DIFF)
  echo "$f lane-side:$l main-side:$m"
done
echo "whole PR diff patch-id: base->lane-tip vs main->merge"
a=$(git diff "$MB" "$L" | git patch-id --stable | cut -d' ' -f1); b=$(git diff "$B" "$M" | git patch-id --stable | cut -d' ' -f1)
echo "  $a / $b"
git diff --shortstat "$B" "$M"; git diff --shortstat "$MB" "$L"

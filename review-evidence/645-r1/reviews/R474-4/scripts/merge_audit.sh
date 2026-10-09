#!/bin/sh
# Merge-composition audit for PR #672 round 2e (R474-4).
# Usage: merge_audit.sh <repo>   (run against a clone that has both parents)
# Checks that the --no-ff merge 9a0d68e2 equals, path by path, one of its two
# parents: every path differing from the dev parent is a lane path and equals
# the lane parent, and every path differing from the lane parent is a dev path
# and equals the dev parent. Prints gitlinks at both parents and the merge.
set -eu
repo=${1:?repo}
cd "$repo"
merge=9a0d68e2016c0385171107277721aa187ce19674
lane=2525eae9567865a8bc741901914bdf5a1caf2c26
dev=99e4eb6c14462aafa84bb1ac597fd241abc1a240
head=85db353400c6bf3965d279a9f5b5d47e08a0d1ed
tmp=$(mktemp -d)
trap 'rm -r "$tmp"' EXIT
base=$(git merge-base "$lane" "$dev")
echo "merge parents: $(git log -1 --format=%P "$merge")"
echo "merge-base: $base"
git diff --name-only "$base" "$lane" | sort > "$tmp/lane"
git diff --name-only "$base" "$dev" | sort > "$tmp/dev"
git diff --name-only "$dev" "$merge" | sort > "$tmp/m_dev"
git diff --name-only "$lane" "$merge" | sort > "$tmp/m_lane"
echo "lane paths: $(wc -l < "$tmp/lane"); dev paths: $(wc -l < "$tmp/dev")"
echo "paths changed on both sides: $(comm -12 "$tmp/lane" "$tmp/dev" | wc -l)"
echo "merge!=dev outside lane paths: $(comm -23 "$tmp/m_dev" "$tmp/lane" | wc -l)"
echo "merge!=lane outside dev paths: $(comm -23 "$tmp/m_lane" "$tmp/dev" | wc -l)"
echo "lane paths where merge!=lane: $(comm -12 "$tmp/m_lane" "$tmp/lane" | wc -l)"
echo "dev paths where merge!=dev: $(comm -12 "$tmp/m_dev" "$tmp/dev" | wc -l)"
for c in "$lane" "$dev" "$merge" "$head"; do
    echo "gitlinks at $c:"
    git ls-tree "$c" protocol-processor gptp-processor third_party/verilog-axis
done
echo "head commit files (merge..head):"
git diff --stat "$merge" "$head" | cat
echo "lane HDL at head vs lane parent (expect empty):"
git diff --stat "$lane" "$head" -- hdl/milan/milan_datapath.sv hdl/ieee1722/aaf/KL_chan_map_capture.sv | cat

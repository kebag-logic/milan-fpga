#!/usr/bin/env bash
# GoogleTest case names (suite.name, macro-level, TEST/TEST_F/TEST_P) of dev's firmware tests and of the head's
# firmware tests plus the pinned stack's tests; prints every dev case the head side lacks.
# usage: test_names.sh <milan repo> <dev rev> <head rev> <stack repo> <stack rev>
set -u
repo=$1 dev=$2 head=$3 stack=$4 srev=$5
names() { tr '\n' ' ' | grep -oE '\b(TEST|TEST_F|TEST_P)\s*\(\s*[A-Za-z0-9_]+\s*,\s*[A-Za-z0-9_]+' | sed -E 's/^[A-Z_]+\s*\(\s*//; s/\s*,\s*/./'; }
list() { local r=$1 rev=$2 dir=$3; git -C "$r" ls-tree -r --name-only "$rev" -- "$dir" | grep -E '\.(cpp|hpp)$' | while read -r f; do git -C "$r" show "$rev:$f" | names; done; }
list "$repo" "$dev" sw/firmware/ctrl/test | sort -u > /tmp/r584-dev-names.$$
{ list "$repo" "$head" sw/firmware/ctrl/test; list "$stack" "$srev" tests; } | sort -u > /tmp/r584-head-names.$$
echo "dev cases: $(wc -l < /tmp/r584-dev-names.$$)  head+stack cases: $(wc -l < /tmp/r584-head-names.$$)"
echo "dev cases missing at head+stack:"; comm -23 /tmp/r584-dev-names.$$ /tmp/r584-head-names.$$
echo "cases new at head+stack:"; comm -13 /tmp/r584-dev-names.$$ /tmp/r584-head-names.$$
rm -f /tmp/r584-*-names.$$

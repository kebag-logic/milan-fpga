#!/usr/bin/env bash
# Pre-existing O-1 check: run the checker from a repository subdirectory on a
# linear branch whose root-level edit never landed.  Usage: probe_subdir.sh <checker> <workdir>
set -eu
checker=$1 w=$2
rm -rf "$w"; mkdir -p "$w"; cd "$w"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null PYTHONDONTWRITEBYTECODE=1
git init -q -b main; git config user.name P; git config user.email p@example.invalid
mkdir sub; echo keep > sub/keep.txt; echo old > root.txt; git add -A; git commit -qm O
git checkout -qb pr; echo new > root.txt; git commit -qam "edit root.txt"
git checkout -q main; echo more > sub/other.txt; git add -A; git commit -qm unrelated
echo "from root:";   rc=0; python3 "$checker" --no-fetch --base main pr || rc=$?; echo "rc=$rc"
cd sub
echo "from sub/:";   rc=0; python3 "$checker" --no-fetch --base main pr || rc=$?; echo "rc=$rc"

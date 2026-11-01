#!/usr/bin/env bash
# Replay rtl-fast `changes` act-path classification offline (.github/workflows/rtl-fast.yml:50-58).
# usage: probe_act_classifier.sh <source-clone> <scratch-dir> <dev-sha> <pr-head-sha>
set -euo pipefail
src=$1; s=$2; dev=$3; head=$4
rm -rf "$s/probe"; git clone -q --no-checkout "$src" "$s/probe"; cd "$s/probe"
git update-ref refs/remotes/origin/dev "$dev"; git checkout -q --detach "$head"
base="$(git merge-base --all refs/remotes/origin/dev "$head")"; echo "base=$base"
git cat-file -e "$base^{commit}"
merged="$(git merge-tree --write-tree refs/remotes/origin/dev "$head")"; echo "merged=$merged"
git diff --no-renames --name-only refs/remotes/origin/dev "$merged" > "$s/changed-files"; wc -l < "$s/changed-files"
python3 -I scripts/ci_scope.py < "$s/changed-files"; echo rc=$?

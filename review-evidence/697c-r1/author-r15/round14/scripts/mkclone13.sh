#!/usr/bin/env bash
# Scratch: a clean clone of the lane at a given revision (default HEAD), every submodule that revision records
# among the lane's five, each from the lane's own checkout (which holds both sides' pins).
# usage: mkclone13.sh <directory> [revision]
set -euo pipefail
lane=$LANES/697-consume
dir=$1; rev=${2:-HEAD}
rm -rf "$dir"
git clone -q "$lane" "$dir"
cd "$dir"
git checkout -q --detach "$(git -C "$lane" rev-parse "$rev^{commit}")"
subs=()
for sub in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  if git ls-files --stage -- "$sub" | grep -q '^160000'; then
    git config "submodule.$sub.url" "$lane/$sub"; subs+=("$sub")
  fi
done
git -c protocol.file.allow=always submodule update -q --init "${subs[@]}"
git log --oneline -1
git submodule status
git status --short | head -5

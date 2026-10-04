#!/usr/bin/env bash
# Usage: run_probe.sh <repo> <commit> <patch|none> <make-target> <name>
# Exports <commit> from <repo> into scratch/probe-<name>, applies <patch>
# with git apply (refusing drift), runs `make -C tb/pp_top <target>` with the
# pinned simulator, and keeps logs/probe-<name>.log and .rc.
set -u
P=$REVIEWS/pp81-r468-3-packet
repo=$1 commit=$2 patch=$3 target=$4 name=$5
. "$P/scripts/env.sh"
d="$P/scratch/probe-$name"
rm -rf "$d"; mkdir -p "$d"
git -C "$repo" archive "$commit" | tar -x -C "$d"
if [ "$patch" != none ]; then
  (cd "$d" && git apply --check "$patch" && git apply "$patch") || { echo 99 > "$P/receipts/runs/probe-$name.rc"; exit 99; }
fi
make -C "$d/tb/pp_top" "$target" > "$P/receipts/runs/probe-$name.log" 2>&1
echo $? > "$P/receipts/runs/probe-$name.rc"

#!/usr/bin/env bash
# Run one mutation-campaign driver in TREE with the pinned simulator first on
# PATH and its scratch copies under TMPDIR; keep stdout+stderr and rc under OUT.
# usage: campaign.sh TREE OUT NAME DRIVER [ARGS...]   (SIM_BIN, TMPDIR from env)
set -u
tree=$1; out=$2; name=$3; shift 3
export PATH="${SIM_BIN:?}:$PATH"
mkdir -p "$out"
cd "$tree" || exit 2
"$@" >"$out/$name.log" 2>&1
echo $? >"$out/$name.rc"

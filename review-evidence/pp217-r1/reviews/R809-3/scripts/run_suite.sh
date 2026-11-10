#!/bin/sh
# Usage: run_suite.sh <repo> <commit> <suite-dir-under-tb> <work-root> <receipt-dir> [make-target]
# Extracts the exact commit's tree with git archive and runs one suite's make, with
# the pinned Verilator through vl.sh. Writes <suite>.log and <suite>.rc.
set -u
repo=$1; c=$2; s=$3; work=$4; rec=$5; tgt=${6:-}
here=$(cd "$(dirname "$0")" && pwd)
tag=$s${tgt:+-$tgt}
w=$work/$tag; rm -rf "$w"; mkdir -p "$w"
git -C "$repo" archive "$c" | tar -x -C "$w"
{ echo "commit $(git -C "$repo" rev-parse "$c") tree $(git -C "$repo" rev-parse "$c^{tree}")"
  "$here/vl.sh" --version; date -u +%FT%TZ
  cd "$w/tb/$s" && make VERILATOR="$here/vl.sh" $tgt; echo "make rc=$?"; date -u +%FT%TZ
} > "$rec/$tag.log" 2>&1
tail -1 "$rec/$tag.log" >/dev/null
grep -o 'make rc=[0-9]*' "$rec/$tag.log" | tail -1 | cut -d= -f2 > "$rec/$tag.rc"

#!/usr/bin/env bash
# Run each gate in gates.txt from the candidate checkout, in parallel, one log and rc per gate.
# usage: run_gates.sh <checkout> <gates.txt> <outdir> <verilator-bin-dir> [jobs]
set -u
co=$1; list=$2; out=$3; vbin=$4; jobs=${5:-16}
mkdir -p "$out"
export PATH="$vbin:$PATH" PYTHONDONTWRITEBYTECODE=1
run_one() {
  name=${1%%|*}; cmd=${1#*|}
  ( cd "$co" && bash -c "$cmd" ) >"$out/$name.log" 2>&1
  echo $? >"$out/$name.rc"
}
export -f run_one; export co out
grep -v '^\s*$' "$list" | tr '\n' '\0' | xargs -0 -P "$jobs" -I{} bash -c 'run_one "$1"' _ {}
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2 >"$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"

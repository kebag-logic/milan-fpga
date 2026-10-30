#!/usr/bin/env bash
# Run the named suites of one checkout, NJ at a time; each suite's make log and
# its last tally line go under <outdir>.  usage: suites.sh <checkout> <outdir> <nj> suite...
set -u
tree=$1; out=$2; nj=$3; shift 3; mkdir -p "$out"
here=$(cd "$(dirname "$0")" && pwd)
one() {
  d=$1; s=$(basename "$d")
  ( cd "$d" && make VERILATOR="$VW" ) >"$OUT/$s.log" 2>&1; rc=$?
  t=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$OUT/$s.log" | tail -1)
  echo "$s rc=$rc tally=[$t]"
}
export -f one; export OUT=$out VW=$here/vwrap.sh
printf '%s\n' "$@" | sed "s#^#$tree/tb/#" | xargs -P "$nj" -I{} bash -c 'one {}' | sort | tee "$out/summary.txt"

#!/usr/bin/env bash
# Run one focused processor suite (its default `make` target, as
# scripts/run_suites.sh does) in an exported tree and record exit status,
# wall time and every tally line. Usage:
#   run_suites_focused.sh <processor-tree> <label> <suite> <outdir>
set -u
tree=$1; label=$2; suite=$3; out=$4
mkdir -p "$out"
log="$out/$label-$suite.log"
cd "$tree/tb/$suite" || exit 2
start=$(date +%s)
make > "$log" 2>&1
rc=$?
end=$(date +%s)
{
  echo "suite $suite label $label exit $rc wall_s $((end - start)) verilator $(verilator --version)"
  grep -E '[0-9]+ checks' "$log"
} > "$out/$label-$suite.tally"
cat "$out/$label-$suite.tally"

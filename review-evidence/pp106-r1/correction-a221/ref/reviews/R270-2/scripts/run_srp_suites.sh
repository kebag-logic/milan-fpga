#!/usr/bin/env bash
# Usage: run_srp_suites.sh <exported-tree> <label> [suite...]
# Builds and runs the SRP Verilator suites of an exported tree with the pinned
# simulator; -j 8 per build, one build at a time. Prints one tally per suite.
set -uo pipefail
tree=$1; label=$2; shift 2
suites=${*:-srp_decoder srp_encoder srp_stream_fsms srp_top}
V=${VERILATOR:-verilator}   # this round: VERILATOR=<pinned 5.050 wrapper>, receipts/00
for s in $suites; do
  d=$tree/tb/$s
  [ -d "$d" ] || { echo "$label $s MISSING"; continue; }
  sed -i 's/--build -j 0/--build -j 8/' "$d/Makefile"
  log=$d/run.log
  rm -rf "$d/obj_dir"
  if (cd "$d" && make VERILATOR="$V") >"$log" 2>&1; then rc=0; else rc=$?; fi
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1)
  echo "$label $s rc=$rc ${tally:-NO-TALLY}"
  grep -E '^FAIL' "$log" | head -40 | sed "s/^/    /"
done

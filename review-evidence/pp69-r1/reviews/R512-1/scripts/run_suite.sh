#!/bin/bash
# run_suite.sh <tree> <suite> <tag> : run `make` (the suite's default target)
# in <tree>/tb/<suite> with the pinned Verilator; log and rc under receipts/runs.
set -u
P=$REVIEWS/pp69-r512-1-packet
tree=$1; suite=$2; tag=$3
log=$P/receipts/runs/$tag-$suite.log
cd "$tree/tb/$suite" || exit 2
start=$(date +%s)
make VERILATOR=$P/scripts/vl_j8.sh >"$log" 2>&1
rc=$?
echo "rc=$rc seconds=$(( $(date +%s) - start ))" > "$P/receipts/runs/$tag-$suite.rc"

#!/bin/bash
# Run the whole suite-cancellation test from one mutant tree; log, rc and wall time per mutant.
# Usage: run_whole.sh <mutant tree> <receipt dir>.  Launch without SIGHUP ignored (no nohup).
tree=$1; out=$2; name=$(basename "$tree")
start=$(date +%s.%N)
(cd "$tree" && env -u PYTHONPATH python3 -B scripts/test_suite_cancellation.py) > "$out/$name.log" 2>&1
echo $? > "$out/$name.rc"
echo "$(date +%s.%N) - $start" | bc > "$out/$name.wall"

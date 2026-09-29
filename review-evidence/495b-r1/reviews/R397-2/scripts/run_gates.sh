#!/bin/bash
# Run each gate command line from a list file (one per line) in the current
# checkout, sequentially, recording rc, elapsed time and the output tail.
# Usage: run_gates.sh <list> <receipt-dir> <prefix>
list=$1 out=$2 prefix=$3
summary="$out/${prefix}_summary.txt"; : > "$summary"
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  i=$((i+1)); log="$out/${prefix}_$(printf %02d $i).log"
  s=$(date +%s)
  { echo "\$ $cmd"; bash -c "$cmd" 2>&1; echo "rc=$?"; } > "$log" 2>&1
  rc=$(tail -1 "$log")
  echo "$(printf %02d $i) ${rc} $(( $(date +%s)-s ))s :: $cmd" | tee -a "$summary"
done < "$list"

#!/bin/sh
# Run named testbench suites of one scratch extraction with the pinned
# simulator; one receipt per suite plus an rc summary line.
# usage: run_suites.sh <tree-name> <suite> [<suite>...]   (runs in parallel)
set -u
PKT=$(cd "$(dirname "$0")/.." && pwd)
TREE=$PKT/scratch/$1; shift
PINNED=${R375_PINNED_BIN:-$VALIDATION_STORAGE/pp127-manager-00b5c6c9/pinned-tool-bin}
OUT=$PKT/receipts
name=$(basename "$TREE")
for s in "$@"; do
  (
    start=$(date +%s)
    PATH=$PINNED:$PATH make -C "$TREE/tb/$s" > "$OUT/$name-suite-$s.log" 2>&1
    rc=$?
    echo "$name $s rc=$rc secs=$(( $(date +%s) - start )) $(grep -E '[0-9]+ checks: ' "$OUT/$name-suite-$s.log" | tail -1)" \
      >> "$OUT/$name-suites-rc.txt"
  ) &
done
wait

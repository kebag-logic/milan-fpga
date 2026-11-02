#!/usr/bin/env bash
# usage: compare.sh <source checkout> <before sha> <after sha> <work dir> <receipts dir> <suite runs per tree> <lifecycle runs per tree>
# Runs both trees at the same moment on the same CPUs, each run in its own
# user+PID namespace, one log and rc per run, never piped.
set -u
src=$1; before=$2; after=$3; work=$4; out=$5; ns=$6; nl=$7
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work" "$out"
NS="unshare --user --map-current-user --pid --fork --kill-child --mount-proc"
for tree in before after; do
  sha=$before; [ $tree = after ] && sha=$after
  "$here/clone_at.sh" "$src" "$sha" "$work/$tree"
done
cat /proc/loadavg > "$out/loadavg-start.txt"
i=0
for tree in before after; do
  for n in $(seq 1 "$ns"); do
    ( cd "$work/$tree" && { echo "# tree $tree head $(git rev-parse HEAD) suite run $n"; PYTHONDONTWRITEBYTECODE=1 timeout -k 5 400 $NS python3 scripts/test_suite_cancellation.py; } > "$out/$tree-suite-$n.log" 2>&1; echo $? > "$out/$tree-suite-$n.rc" ) &
  done
  for n in $(seq 1 "$nl"); do
    ( cd "$work/$tree/tb/verilator/gptp_shadow" && { echo "# tree $tree head $(git rev-parse HEAD) lifecycle run $n"; PYTHONDONTWRITEBYTECODE=1 timeout -k 5 400 $NS python3 test_mutant_lifecycle.py; } > "$out/$tree-lifecycle-$n.log" 2>&1; echo $? > "$out/$tree-lifecycle-$n.rc" ) &
  done
done
sleep 20; cat /proc/loadavg > "$out/loadavg-during.txt"
wait
cat /proc/loadavg > "$out/loadavg-end.txt"

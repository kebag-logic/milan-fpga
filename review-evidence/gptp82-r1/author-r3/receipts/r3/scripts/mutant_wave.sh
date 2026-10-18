#!/bin/bash
# Shards K..K+W-1 of N of the engine mutation arm, in parallel, each the
# suite's own main() over MUTATIONS[k::N] with the clean control.
# Usage: mutant_wave.sh TREE OUT N FIRST COUNT
set -u
TREE=$1 OUT=$2 N=$3 FIRST=$4 COUNT=$5
export PATH=<tools>/pinned-verilator-5.050:$PATH
export TMPDIR=<scratch>/tmpdir
mkdir -p "$OUT"
S=<scratch>/r3/scripts/shard_mutants.py
pids=()
for ((k=FIRST; k<FIRST+COUNT && k<N; k++)); do
  ( python3 "$S" "$TREE/tb/verilator/engine" $k $N > "$OUT/engine-mutants-s$k.log" 2>&1
    echo $? > "$OUT/engine-mutants-s$k.rc" ) &
  pids+=($!)
done
for p in "${pids[@]}"; do wait $p; done
for ((k=FIRST; k<FIRST+COUNT && k<N; k++)); do
  echo "s$k rc=$(cat "$OUT/engine-mutants-s$k.rc") $(grep -E '^[0-9]+ checks:' "$OUT/engine-mutants-s$k.log")"
done

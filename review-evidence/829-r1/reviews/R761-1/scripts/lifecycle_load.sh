#!/usr/bin/env bash
# lifecycle_load.sh <packet> <probe root> <repeats> <burners>: gptp_shadow's process-cleanup lifecycle test,
# head and base side by side under one CPU load, each with its own log and rc file.
P=$1 T=$2 N=$3 B=$4; L=$P/receipts/run/lifecycle; mkdir -p "$L"
export TMPDIR=$P/scratch/tmp PATH=$(dirname "${VERILATOR:-$TOOLS/pinned-verilator-5.050/verilator}"):$PATH
pids=(); for ((i=0;i<B;i++)); do python3 -I -c 'while True: pass' & pids+=($!); done
jobs_=()
for side in tree basetree; do
  for ((r=1;r<=N;r++)); do
    ( cd "$T/$side/tb/verilator/gptp_shadow" && s=$(date +%s); python3 test_mutant_lifecycle.py > "$L/$side-$r.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s" > "$L/$side-$r.rc" ) &
    jobs_+=($!)
  done
done
wait "${jobs_[@]}"
kill "${pids[@]}" 2>/dev/null

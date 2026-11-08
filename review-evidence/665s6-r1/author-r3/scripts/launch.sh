#!/bin/bash
# launch.sh NAME CPUS -- RUN_JOB_ARGS... [;; RUN_JOB_ARGS...]: one unit, milan-665s6-a745c-NAME, on CPUS,
# running run_job.py once per ';;'-separated argument list, in order; its output in $ROOT/units/NAME.log.
set -euo pipefail
name=$1; cpus=$2; shift 3
ROOT=$VALIDATION_STORAGE/scratch/665s6-a745c/replay
mkdir -p "$ROOT/units"
batch="$ROOT/units/$name.batch"
: > "$batch"
cur=()
for a in "$@"; do
  if [ "$a" = ";;" ]; then printf '%s\n' "${cur[*]}" >> "$batch"; cur=(); else cur+=("$a"); fi
done
[ ${#cur[@]} -gt 0 ] && printf '%s\n' "${cur[*]}" >> "$batch"
systemd-run --user --unit="milan-665s6-a745c-$name" --collect --property=MemoryMax=10G \
  --property=StandardOutput="file:$ROOT/units/$name.log" --property=StandardError="file:$ROOT/units/$name.log" \
  --setenv=REPLAY_NEEDS="${REPLAY_NEEDS:-{\}}" --setenv=YOSYS_RESULT_ROOTS="${YOSYS_RESULT_ROOTS:-}" \
  /usr/bin/taskset -c "$cpus" /usr/bin/python3 $HOME/milan-fpga-management/2026-09-23/665s6-a745c/scripts/run_batch.py "$batch"

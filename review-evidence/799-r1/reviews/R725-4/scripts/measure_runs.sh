#!/bin/sh
# Usage: measure_runs.sh <clone> <scratch> RUN...
# Converts raw per-job logs (jobs/{id}/logs API: "TIMESTAMP message") into the
# `gh run view --log` shape ("job<TAB>step<TAB>TIMESTAMP message") the head's
# --measure reads, then measures each run and the union with the head's own code.
set -eu
clone=$1; scratch=$2; shift 2
all=""
for run in "$@"; do
  mkdir -p "$scratch/conv-$run"
  files=""
  for f in "$scratch/logs-$run"/shard-*.log; do
    out="$scratch/conv-$run/$(basename "$f")"
    sed 's/^/job\tstep\t/' "$f" > "$out"
    files="$files $out"
  done
  echo "== run $run"
  python3 -I "$clone/scripts/suite_shards.py" --measure $files
  all="$all $files"
done
echo "== union $*"
python3 -I "$clone/scripts/suite_shards.py" --measure $all

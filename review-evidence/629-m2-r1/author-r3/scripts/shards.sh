#!/bin/bash
# The five verilator-shards workers in sequence (one sweep per tree), shard 3 last.
set -u
R=$VALIDATION_STORAGE/629-a500
head=$(git -C $LANES/629-m2-impl rev-parse HEAD)
for s in 0 1 2 4 3; do
  echo "shard $s start $(date -Is)"
  "$R/replay/run_job.sh" .github/workflows/rtl.yml verilator-shards "vshard$s" \
    --matrix "shard=$s" --matrix total=5 \
    --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true
  echo "shard $s rc=$? end $(date -Is)"
done

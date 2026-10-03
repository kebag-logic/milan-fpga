#!/bin/bash
# The five verilator-shards workers in sequence (one sweep per tree: the
# sweep's per-tree lock refuses a second), then the verilator-suites
# aggregate over this replay's own shard logs.
set -u
R=$VALIDATION_STORAGE/629-a512
O=$HOME/milan-fpga-management/2026-09-23/629-a512/scripts
mkdir -p "$R/home-shards"
head=$(git -C $LANES/629-m2-impl rev-parse HEAD)
all=success
for s in 0 1 2 4 3; do
  echo "shard $s start $(date -Is)"
  HOMEDIR=$R/home-shards "$O/run_job.sh" .github/workflows/rtl.yml verilator-shards "vshard$s" \
    --matrix "shard=$s" --matrix total=5 \
    --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true
  rc=$?
  [ $rc = 0 ] || all=failure
  echo "shard $s rc=$rc end $(date -Is)"
done
seeds=()
for s in 0 1 2 3 4; do seeds+=(--seed "all-suite-logs/suite-logs-$s=$R/replay/vshard$s/runner_temp/suite-logs"); done
echo "verilator-suites start $(date -Is)"
HOMEDIR=$R/home-shards "$O/run_job.sh" .github/workflows/rtl.yml verilator-suites verilator-suites \
  --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true \
  --value needs.full-ci-gate.result=success --value "needs.verilator-shards.result=$all" "${seeds[@]}"
echo "verilator-suites rc=$? end $(date -Is)"

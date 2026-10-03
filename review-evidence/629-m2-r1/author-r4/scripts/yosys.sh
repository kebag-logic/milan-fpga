#!/bin/bash
# rtl-fast's yosys-elaboration, then rtl.yml's four yosys-shards workers in
# sequence, then the yosys-portability aggregate over their evidence.
set -u
R=$VALIDATION_STORAGE/629-a512
O=$HOME/milan-fpga-management/2026-09-23/629-a512/scripts
head=$(git -C $LANES/629-m2-impl rev-parse HEAD)
mkdir -p "$R/home-yosys"
echo "yosys-elaboration start $(date -Is)"
HOMEDIR=$R/home-yosys "$O/run_job.sh" .github/workflows/rtl-fast.yml yosys-elaboration rf-yosys-elab \
  --needs changes.rtl=true
echo "yosys-elaboration rc=$? end $(date -Is)"
all=success
for s in 0 1 2 3; do
  echo "yosys shard $s start $(date -Is)"
  HOMEDIR=$R/home-yosys "$O/run_job.sh" .github/workflows/rtl.yml yosys-shards "yshard$s" \
    --matrix "shard=$s" --matrix total=4 \
    --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true
  rc=$?
  [ $rc = 0 ] || all=failure
  echo "yosys shard $s rc=$rc end $(date -Is)"
done
seeds=()
for s in 0 1 2 3; do seeds+=(--seed "all-yosys-results/yosys-results-$s=$R/replay/yshard$s/runner_temp/yosys-results"); done
echo "yosys-portability start $(date -Is)"
HOMEDIR=$R/home-yosys "$O/run_job.sh" .github/workflows/rtl.yml yosys-portability yosys-portability \
  --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true \
  --value needs.full-ci-gate.result=success --value "needs.yosys-shards.result=$all" \
  --value needs.verilator-suites.result=success "${seeds[@]}"
echo "yosys-portability rc=$? end $(date -Is)"

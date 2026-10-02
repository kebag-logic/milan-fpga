#!/bin/bash
# rtl-fast's yosys-elaboration, then rtl.yml's four yosys-shards workers, in sequence.
set -u
R=$VALIDATION_STORAGE/629-a500
head=$(git -C $LANES/629-m2-impl rev-parse HEAD)
mkdir -p "$R/home-yosys"
echo "yosys-elaboration start $(date -Is)"
HOMEDIR=$R/home-yosys "$R/replay/run_job.sh" .github/workflows/rtl-fast.yml yosys-elaboration rf-yosys-elab \
  --needs changes.rtl=true
echo "yosys-elaboration rc=$? end $(date -Is)"
for s in 0 1 2 3; do
  echo "yosys shard $s start $(date -Is)"
  HOMEDIR=$R/home-yosys "$R/replay/run_job.sh" .github/workflows/rtl.yml yosys-shards "yshard$s" \
    --matrix "shard=$s" --matrix total=4 \
    --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true
  echo "yosys shard $s rc=$? end $(date -Is)"
done

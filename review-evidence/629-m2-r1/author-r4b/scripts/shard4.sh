#!/bin/bash
# rtl.yml's verilator-shards worker 4 of 5, the shard that holds milan_dp,
# replayed at the lane head under GNU make 4.3 in its own HOME.
set -u
R=$VALIDATION_STORAGE/629-a517
O=$HOME/milan-fpga-management/2026-09-23/629-a517/scripts
mkdir -p "$R/home-shards" "$R/replay"
head=$(git -C $LANES/629-m2-impl rev-parse HEAD)
echo "shard 4 start $(date -Is) head $head"
HOMEDIR=$R/home-shards "$O/run_job.sh" .github/workflows/rtl.yml verilator-shards vshard4 \
  --matrix shard=4 --matrix total=5 \
  --needs "full-ci-gate.target_sha=$head" --needs full-ci-gate.run_full=true
echo "shard 4 rc=$? end $(date -Is)"

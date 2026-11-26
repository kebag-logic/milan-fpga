#!/bin/sh
# usage: fw_shards.sh <repo> <logdir> <cpus> : firmware gate shards 0 and 1 in sequence
repo=$1; logdir=$2; cpus=$3; runner=$(dirname "$0")/run_suite.sh
for k in 0 1; do
  "$runner" fw_shard$k "$cpus" "$repo" "$logdir" python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $k/4
done

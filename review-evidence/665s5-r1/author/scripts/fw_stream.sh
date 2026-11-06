#!/bin/bash
# Run firmware self-test shards one after another in a clone, each its own gate log.
# usage: fw_stream.sh CLONE GATEDIR SHARD...
S=$MANAGEMENT/2026-09-23/665s5-a702/scripts
C=$1 G=$2; shift 2
for k in "$@"; do
  bash $S/gate.sh "$C" "$G/selftest-shard$k.log" . python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard $k/4 --jobs 8
done

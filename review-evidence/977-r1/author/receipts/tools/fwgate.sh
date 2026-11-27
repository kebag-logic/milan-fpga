#!/bin/bash
# fwgate.sh CLONE K: the firmware gate's shard K of 4 in CLONE, as CI runs it.
cd "$1" && python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard "$2/4"

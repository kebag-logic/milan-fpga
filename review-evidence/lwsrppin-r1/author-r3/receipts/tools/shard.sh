#!/bin/bash
# shard.sh K OUTDIR: one firmware gate shard at the lane head, its start, end and rc recorded.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
k=$1; o=$2; cd /data-2/milan/lanes/lwsrp-pin || exit 9
date -Iseconds > $o/start-$k; git rev-parse HEAD > $o/head-$k
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard $k/4 --jobs 4 --build-dir $o/build-$k > $o/gate-$k.log 2>&1
echo $? > $o/rc-$k; date -Iseconds > $o/end-$k

#!/bin/bash
# harness1.sh NAME POINT VARIANT: one CPU budget harness run at the lane head, as round 1's harness.sh runs each.
source /data-2/milan/tmp/lwsrppin-a834/r4/bin/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/r4/harness; cd /data-2/milan/lanes/lwsrp-pin || exit 9
n=$1; p=$2; v=$3
date -Iseconds > $o/start-$n; git rev-parse HEAD > $o/head-$n
python3 -B tb/verilator/ctrl_service_budget/run.py --point $p --build-dir $o/b-$n --variant $v \
  --record-budget-findings --record-share-findings > $o/run-$n.log 2>&1
echo $? > $o/rc-$n; date -Iseconds > $o/end-$n

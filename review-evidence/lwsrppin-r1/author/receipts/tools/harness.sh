#!/bin/bash
# harness.sh NAME POINT VARIANT [NAME POINT VARIANT ...]: CPU budget harness runs in sequence at the lane head.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/harness; cd /data-2/milan/lanes/lwsrp-pin || exit 9
while [ $# -ge 3 ]; do
  n=$1; p=$2; v=$3; shift 3
  date -Iseconds > $o/start-$n; git rev-parse HEAD > $o/head-$n
  python3 -B tb/verilator/ctrl_service_budget/run.py --point $p --build-dir $o/b-$n --variant $v \
    --record-budget-findings --record-share-findings > $o/run-$n.log 2>&1
  echo $? > $o/rc-$n; date -Iseconds > $o/end-$n
done

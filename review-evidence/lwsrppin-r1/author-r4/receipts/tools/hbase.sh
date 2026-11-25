#!/bin/bash
# hbase.sh: arm A's backlog-owed and srp-bound groups at 8x8/1if on the train's own image (2509db68), the base worktree.
source /data-2/milan/tmp/lwsrppin-a834/r4/bin/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/r4/harness; n=base-8x8-1if; cd /data-2/milan/tmp/lwsrppin-a834/base || exit 9
date -Iseconds > $o/start-$n; git rev-parse HEAD > $o/head-$n; git status --porcelain | wc -l > $o/porcelain-$n
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir $o/b-$n --groups backlog-owed,srp-bound \
  --record-budget-findings --record-share-findings > $o/run-$n.log 2>&1
echo $? > $o/rc-$n; date -Iseconds > $o/end-$n

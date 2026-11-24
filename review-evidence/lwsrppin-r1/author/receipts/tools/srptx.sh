#!/bin/bash
# srptx.sh NAME TREE: make -k srptx, then srptx-mutants, in TREE's milan_dp, rc and times recorded.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
n=$1; o=/data-2/milan/tmp/lwsrppin-a834/srptx; cd $2/tb/verilator/milan_dp || exit 9
git rev-parse HEAD > $o/head-$n; git -C ../../../third_party/lwSRP rev-parse HEAD > $o/lwsrp-$n
for t in srptx srptx-mutants; do
  date -Iseconds > $o/start-$n-$t; make -k $t > $o/$n-$t.log 2>&1; echo $? > $o/rc-$n-$t; date -Iseconds > $o/end-$n-$t
done

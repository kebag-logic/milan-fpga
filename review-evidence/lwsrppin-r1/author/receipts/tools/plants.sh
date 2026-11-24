#!/bin/bash
# plants.sh OUTDIR: make twin, then make twin-plants twice, at the lane head under the pinned tools.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=$1; cd /data-2/milan/lanes/lwsrp-pin/tb/verilator/milan_dp || exit 9
git rev-parse HEAD > $o/head; verilator --version > $o/verilator
for n in twin plants-1 plants-2; do
  t=twin-plants; [ $n = twin ] && t=twin
  date -Iseconds > $o/start-$n; make $t > $o/$n.log 2>&1; echo $? > $o/rc-$n; date -Iseconds > $o/end-$n
done

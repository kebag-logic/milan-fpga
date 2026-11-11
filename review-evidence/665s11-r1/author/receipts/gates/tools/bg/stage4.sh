#!/bin/bash
# stage4.sh: start pass4's S2, builder and census groups once elaborate-gates-1 has finished, so its LiteX
# simulations do not share the pool with them
T=<scratch>/tools/bg.sh; G=<scratch>/gates; H=b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702
R=$G/pass4; B=<scratch>/bg
until [ -e $R/logs/elaborate.elaborate-gates-1__DONE ]; do sleep 30; done
echo "$(date +%T) elaborate-gates-1 done; starting s2, build, census"
$T lanes2 $G/tools/lane_gates.sh $H $R s2
$T lanebuild $G/tools/lane_gates.sh $H $R build
systemd-run --user --unit=milan-665s11-a761-census4 --collect -p MemoryMax=10G -p MemoryHigh=9G /usr/bin/taskset -c 96-127 \
  /bin/bash -c "$G/tools/drive.sh $H $R E rtl-fast:publication-census > $B/drvE.log 2>&1; echo \$? > $B/drvE.rc"

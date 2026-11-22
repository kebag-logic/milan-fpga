#!/bin/bash
# hsubset.sh CLONE MEAS POINT JOBS: the groups that read the ENTITY descriptor (the AEM image the flip changes in its
# firmware string) and the boot's control group, at POINT, run.py --reuse-build with the formal measurement's options
# on the arm images hbuild.sh built, into MEAS/<point>/<arm>/subset.
set -u
S=<scratch>; . $S/bin/fwenv.sh
export MAKEFLAGS="-j2 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 M=$2 P=$3 J=$4; rc=0
run() { local arm=$1 groups=$2; local var=(); [ "$arm" != none ] && var=(--variant "$arm")
  echo "== $P $arm $groups start $(date +%T)"
  python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $M/$P/$arm --reuse-build --out $M/$P/$arm/subset \
    --groups "$groups" --record-budget-findings --record-share-findings --jobs $J "${var[@]}" > $M/$P/$arm.subset.log 2>&1
  local r=$?; echo "== $P $arm rc=$r $(date +%T): $(tail -3 $M/$P/$arm.subset.log | tr '\n' ' ' | cut -c1-220)"; [ $r = 0 ] || rc=1; }
run none control,aecp,aecp-held,aecp-fanout,aecp-largest-notice
run answering-ports aecp-reboot
run declaring-outputs aecp-outputs
echo "END rc=$rc $(date +%T)"; exit $rc

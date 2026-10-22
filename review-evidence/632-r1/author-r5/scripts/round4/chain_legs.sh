#!/usr/bin/env bash
# milan_dp: every ordinary leg but base and notify, one at a time, build then exec
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final/dp_legs
mkdir -p $L
cd $LANES/632-phase/tb/verilator/milan_dp
git rev-parse HEAD > $L/head.txt
for c in crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1; do
  date -Is > $L/$c.start
  make build-$c > $L/$c.build.log 2>&1; echo $? > $L/$c.build.rc
  make exec-$c > $L/$c.log 2>&1; echo $? > $L/$c.rc
  date -Is > $L/$c.end
done
echo DONE > $L/DONE

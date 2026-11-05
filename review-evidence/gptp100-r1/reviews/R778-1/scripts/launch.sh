#!/bin/bash
# usage: launch.sh <packet dir>
# Starts the reviewer's three campaigns detached (nohup), each with its own
# log and rc file, in the probe copy <packet>/scratch/head. TMPDIR is kept
# inside the packet's scratch so tool temp trees stay there.
P=$1; H=$P/scratch/head
export PATH=$P/scratch/bin:$PATH TMPDIR=$P/scratch/tmp
mkdir -p $TMPDIR $P/receipts/engine-run $P/receipts/arm-p100 $P/receipts/suites
( cd $H/tb/verilator/engine && make run > $P/receipts/engine-run/engine-run.log 2>&1; echo $? > $P/receipts/engine-run/rc ) </dev/null >/dev/null 2>&1 &
( cd $P && python3 -I scripts/arm_subset.py $H/tb/verilator/engine $P/scratch/arm-p100 --jobs 8 --p100 --probes > $P/receipts/arm-p100/driver.log 2>&1; echo $? > $P/receipts/arm-p100/rc ) </dev/null >/dev/null 2>&1 &
( cd $H; for t in "make contract" "make -C tb/verilator/ucpu" "make -C tb/verilator/parser" "make -C tb/verilator/gaskets" "make -C tb/tsngen" "make -C bench/arty test" "make lint" "make docs" "make diagrams-check"; do
    n=$(echo $t | tr " /" "__"); s=$(date +%s); $t > $P/receipts/suites/$n.log 2>&1
    echo "$? $(( $(date +%s)-s ))s $t" >> $P/receipts/suites/rc.txt; done
  git status --porcelain > $P/receipts/suites/status-after.txt; echo done > $P/receipts/suites/finished ) </dev/null >/dev/null 2>&1 &

#!/bin/bash
# ledger.sh NAME TREE ARGS...: plat_ledger.py in TREE, its start, end and rc recorded.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
n=$1; t=$2; shift 2; o=/data-2/milan/tmp/lwsrppin-a834/r3/ledger; cd $t || exit 9
date -Iseconds > $o/start-$n; git rev-parse HEAD > $o/head-$n
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $o/b-$n "$@" > $o/$n.log 2>&1
echo $? > $o/rc-$n; date -Iseconds > $o/end-$n

#!/bin/bash
# Round 7: the ledger gates on a tree (test_ctrl_memory.py, plat_ledger.py --self-test, the fixtures). usage: ledger7.sh TREE OUT
set -u
TREE=$1 OUT=$2 T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r4/tmp/ledger7 MAKEFLAGS="-j8 --no-print-directory"; mkdir -p $TMPDIR; rm -rf $OUT; mkdir -p $OUT
cd $TREE
python3 sw/litex/test_ctrl_memory.py > $OUT/ctrl_memory.log 2>&1; echo "ctrl_memory rc=$?" > $OUT/summary.txt
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $OUT/plat-ledger --self-test > $OUT/plat_ledger.log 2>&1; echo "plat_ledger rc=$?" >> $OUT/summary.txt
bash $T/scripts/r4/fixtures3.sh $PWD $OUT/plat-ledger $OUT/fixtures > $OUT/fixtures.log 2>&1; echo "fixtures rc=$?" >> $OUT/summary.txt

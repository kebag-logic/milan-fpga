#!/bin/bash
# Round 7: the composed tree's images before the merge commit (the worktree, its conflicts in code resolved):
# plat_ledger.py --self-test (the platform at the four points against the ledger) and the size fixture at the four
# points (fixtures3.sh), with each image's rom and each ELF's sha256. usage: rom7.sh TREE OUT
set -u
TREE=$1 OUT=$2 T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r4/tmp/rom7 MAKEFLAGS="-j8 --no-print-directory"; mkdir -p $TMPDIR
rm -rf $OUT; mkdir -p $OUT
cd $TREE
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $OUT/plat-ledger --self-test > $OUT/plat_ledger.log 2>&1; echo "plat_ledger rc=$?" > $OUT/summary.txt
bash $T/scripts/r4/fixtures3.sh $PWD $OUT/plat-ledger $OUT/fixtures > $OUT/fixtures.log 2>&1; echo "fixtures rc=$?" >> $OUT/summary.txt
for f in $(find $OUT -name ctrl_app.elf | sort); do echo "${f#$OUT/} $(sha256sum $f | cut -c1-64)"; done >> $OUT/summary.txt

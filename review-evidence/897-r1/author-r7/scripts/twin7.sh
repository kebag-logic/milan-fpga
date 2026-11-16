#!/bin/bash
# Round 7: the milan_dp twin and its plants on a clean clone (make -C tb/verilator/milan_dp twin, twin-plants), as
# lane part a runs them. usage: twin7.sh CLONE OUT
set -u
C=$1 OUT=$2 T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r4/tmp/twin7-$(basename $OUT) MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p $TMPDIR; rm -rf $OUT; mkdir -p $OUT
cd $C
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)" > $OUT/summary.txt
make -C tb/verilator/milan_dp twin > $OUT/twin.log 2>&1; echo "twin rc=$?" >> $OUT/summary.txt
make -C tb/verilator/milan_dp twin-plants > $OUT/twin_plants.log 2>&1; echo "twin_plants rc=$?" >> $OUT/summary.txt
git status --porcelain --untracked-files=no >> $OUT/summary.txt

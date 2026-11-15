#!/bin/bash
# Scratch only (never committed): the platform's images linked at every point on cl-cut, whose path() reads the same
# words in the same order through one gsi() call site, to size what such a cut would save. usage: cut_rom.sh
set -u
T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r4/tmp/cut; mkdir -p $TMPDIR
cd $T/r4/cl-cut || exit 3
rm -rf $T/r4/builds/cut
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $T/r4/builds/cut/plat-ledger --self-test > $T/r4/logs/cut-plat_ledger.log 2>&1
echo "rc=$?" >> $T/r4/logs/cut-plat_ledger.log

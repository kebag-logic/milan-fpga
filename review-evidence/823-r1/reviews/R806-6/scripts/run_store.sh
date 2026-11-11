#!/bin/sh
# Usage: run_store.sh <clone> <packet> <jobs>. The store's host gate with every planted defect, RV32 required.
C=$1; P=$2; J=$3; export TMPDIR=$P/scratch/tmp
cd "$C" || exit 2
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs "$J" > "$P/receipts/store_selftest.log" 2>&1
echo $? > "$P/receipts/store_selftest.rc"

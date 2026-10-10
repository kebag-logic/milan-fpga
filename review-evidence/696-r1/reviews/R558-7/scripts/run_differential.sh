#!/usr/bin/env bash
# [R558] R558-7: firmware MAAP differential self-test at the exact head.
# usage: run_differential.sh <clone> <packet>
C=$1; P=$2; S=$P/scratch
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1
cd "$C" && python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep $S/differential > $P/receipts/differential.log 2>&1; echo $? > $P/receipts/differential.rc

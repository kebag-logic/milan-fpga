#!/usr/bin/env bash
# [R558] R558-7: the repository's MAAP planted-defect campaign at the exact head.
# usage: run_campaign.sh <clone> <packet>
C=$1; P=$2; S=$P/scratch
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp VERILATOR_JOBS=4
ln -sf "$C/tb/verilator/maap/mutants.py" $S/r558_maap_campaign.py
cd "$C/tb/verilator/maap" && python3 $S/r558_maap_campaign.py > $P/receipts/mutants.log 2>&1; echo $? > $P/receipts/mutants.rc

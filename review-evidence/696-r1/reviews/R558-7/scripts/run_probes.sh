#!/usr/bin/env bash
# [R558] R558-7: run reviewer probes detached; usage: run_probes.sh <clone> <packet>
P=$2; S=$P/scratch
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp
python3 -I $P/scripts/reviewer_probes.py "$1" $S/probes --jobs 5 > $P/receipts/reviewer_probes.log 2>&1; echo $? > $P/receipts/reviewer_probes.rc

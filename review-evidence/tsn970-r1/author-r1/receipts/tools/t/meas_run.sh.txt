#!/bin/bash
# meas_run.sh CLONE BUILD POINT VARIANT GROUPS JOBS OUT: run.py on a finished build (--reuse-build) of VARIANT for
# GROUPS, recording budget and share findings (the formal measurement's options); rc and times at the end.
set -u
C=$1 B=$2 P=$3 V=$4 G=$5 J=$6 O=$7
cd "$C" || exit 3
echo "HEAD $(git rev-parse --short=8 HEAD) point $P variant $V groups $G jobs $J start $(date +%T)"
python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$B" --reuse-build --variant "$V" \
  --groups "$G" --out "$O" --jobs "$J" --record-budget-findings --record-share-findings
rc=$?; echo "END rc=$rc $(date +%T)"; exit $rc

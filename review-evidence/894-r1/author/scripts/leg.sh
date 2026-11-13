#!/bin/bash
# One measurement leg: run.py at a point on CLONE, into BUILD, with JOBS groups at once. usage: leg.sh CLONE BUILD POINT JOBS [run.py args]
set -u
C=$1 B=$2 P=$3 J=$4; shift 4
T=/data-2/milan/tmp/894-a773
. $T/scripts/env.sh
export MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1 TMPDIR=$T/tmp/$(basename $B)
mkdir -p $B $TMPDIR
echo "HEAD $(git -C $C rev-parse HEAD) DIRTY $(git -C $C status --porcelain --untracked-files=no | wc -l) point $P jobs $J args $* start $(date +%FT%T)"
python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $B --out $B/results --record-budget-findings --record-share-findings --jobs $J "$@"
rc=$?; echo "END rc=$rc $(date +%FT%T)"; exit $rc

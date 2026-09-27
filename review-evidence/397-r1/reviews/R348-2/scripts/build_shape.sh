#!/bin/bash
# Build one shape at the exact head into <scratch>/build-<shape> (foreground).
# usage: build_shape.sh <repo> <scratch> <shape>
set -u
REPO=$1; S=$2; SHAPE=$3
. "$(dirname "$0")/env.sh"
cd "$REPO"
/usr/bin/time -v python -B tb/verilator/fw_service_budget/run.py --shape $SHAPE \
  --build-dir $S/build-$SHAPE --build-only > $S/build-$SHAPE.out 2>&1
echo "build $SHAPE rc=$?" | tee -a $S/build-status.txt

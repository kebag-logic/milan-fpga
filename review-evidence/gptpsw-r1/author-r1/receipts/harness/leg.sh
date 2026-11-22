#!/usr/bin/env bash
# leg.sh <clone> <build-dir> <point> <groups> [run.py options...]: one harness leg, the formal options
set -u; source <scratch>/bin/env.sh
export MAKEFLAGS="-j16 --no-print-directory" PYTHONUNBUFFERED=1
C=$1; B=$2; P=$3; G=$4; shift 4
cd "$C" && python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$B" --groups "$G" \
  --record-budget-findings --record-share-findings "$@"

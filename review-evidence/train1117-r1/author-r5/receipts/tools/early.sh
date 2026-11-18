#!/bin/bash
# early.sh CLONE BUILD POINT OUT GROUPS [VARIANT]: run.py on a leg's existing build (--reuse-build) for a few groups into OUT,
# with the formal measurement's options; the figures arrive before the leg's own part reaches them.
. <scratch>/bin/env.sh
export PYTHONUNBUFFERED=1
python3 -B $1/tb/verilator/ctrl_service_budget/run.py --point $3 --build-dir $2 --reuse-build --out $4 --groups $5 \
  --record-budget-findings --record-share-findings --jobs 2 ${6:+--variant $6}; echo "END rc=$? $(date +%T)"

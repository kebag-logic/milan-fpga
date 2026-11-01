#!/bin/sh
# One 1x1, 4 KiB flash arm over the four backlog windows: run_arm.sh TREE OUTDIR
# Set PACKET, LITEX_VENV, SDK_BIN, VERILATOR_DIR and SV2V_DIR first.
. "$PACKET/scripts/env.sh"
cd "$1" || exit 2
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$2" --xip --fetch-l1 64x1 \
  --groups backlog,backlog-owed,backlog-adp,backlog-adp-refill --jobs 4 --record-budget-findings > "$2.log" 2>&1
echo $? > "$2.rc"

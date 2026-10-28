#!/usr/bin/env bash
# #799: re-run the firmware gate set's ctrl_boundary at <rev> in its clean clone, after the shared RV32 SDK the first
# run's MILAN_RV32_CC named was removed mid-run (exit 127 inside the capture); MILAN_RV32_CC now names this session's
# verified install (fw_env.sh).
# usage: fw_boundary_rerun.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-fw-${rev:0:8}; O=$X/r/firmware-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
cd "$C" || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export HOME=$X/home-fw
s=$(date +%s); "$LITEX_PYTHON" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest > "$O/ctrl_boundary-rerun.log" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s ctrl_boundary (rerun): $LITEX_PYTHON sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest" >> "$O/table.txt"
git status --porcelain --untracked-files=no > "$O/clone-status-after-rerun.txt"
echo FW-BOUNDARY-RERUN-DONE >> "$O/table.txt"

#!/bin/sh
# Reproduces this round's local evidence. Usage: sh run_r935_5.sh <clone at the exact head> <packet dir>
# Reads the clone only; writes receipts under <packet dir>/receipts. Needs python3; the gh steps need read access.
set -u
C=$(cd "$1" && pwd); P=$(cd "$2" && pwd); R="$P/receipts"; mkdir -p "$R"
cd "$C" || exit 2
# 1. the boundary gate's text cross-check, at the head and with the parent head's OUTSIDE table
{ echo "## head $(git rev-parse HEAD)"; python3 -I -B "$P/probe_outside.py" .; echo "rc=$?"
  echo "## OUTSIDE without model_counts.py (the parent head 57f32b28d's table)"
  python3 -I -B "$P/probe_outside.py" . tb/verilator/ctrl_service_budget/model_counts.py; echo "rc=$?"; } > "$R/probe_outside.txt" 2>&1
# 2. the model-count check the new entry names
(cd tb/verilator/ctrl_service_budget && python3 -B model_counts.py; echo "rc=$?") > "$R/model_counts_head.txt" 2>&1
# 3. the parent head's hosted boundary refusal (read-only)
gh run view 45814568764 -R kebag-logic/milan-fpga --job 140054650541 --log-failed 2>&1 | grep -E 'REFUSED' \
  | sed -E 's/^.*Z (REFUSED)/\1/' > "$R/hosted_parent_firmware_boundary_refusal.rerun.txt"
# 4. clone state
{ git rev-parse HEAD HEAD^{tree}; git write-tree; git status --porcelain=v1 --untracked-files=all --ignored
  git submodule status; } > "$R/tree_restore_check.rerun.txt" 2>&1

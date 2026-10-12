#!/usr/bin/env bash
# Usage: run_logged.sh NAME CMD... ; runs CMD from the review clone with the pinned
# Python 3.12.3 venv first on PATH, writing receipts/NAME.log and receipts/NAME.rc.
set -u
PKT=${PKT:-$REVIEWS/716-r620-2-packet}
CLONE=${CLONE:-$REVIEWS/r620-2-716}
name=$1; shift
export PATH="$PKT/scratch/venv312/bin:$PATH"
export TMPDIR="$PKT/scratch/tmp" PYTHONPYCACHEPREFIX="$PKT/scratch/pycache"
export MILAN_RV32_CC="$PKT/scratch/rv32-sdk/bin/riscv32-linux-gcc"
mkdir -p "$TMPDIR" "$PKT/receipts"
cd "$CLONE" || exit 99
start=$(date +%s.%N)
{ echo "# cmd: $*"; echo "# head: $(git rev-parse HEAD)"; echo "# python: $(python3 --version)"; } > "$PKT/receipts/$name.log"
"$@" >> "$PKT/receipts/$name.log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "# rc=$rc wall=$(echo "$end - $start" | bc)" >> "$PKT/receipts/$name.log"
echo "$rc" > "$PKT/receipts/$name.rc"

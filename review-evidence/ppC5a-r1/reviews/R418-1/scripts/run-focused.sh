#!/usr/bin/env bash
# Focused lane suites at the exact head, in a disposable git-archive export.
# Usage: run-focused.sh <clone> <head-sha> <packet-dir>
set -u
CLONE=$1; HEAD=$2; PKT=$3
EXP=$PKT/scratch/focused
rm -rf "$EXP"; mkdir -p "$EXP" "$PKT/receipts"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP"
# cap the C++ build at 8 jobs (scratch copy only)
sed -i 's/--build -j 0/--build -j 8/' "$EXP/tb/pp_top/Makefile" "$EXP/tb/ucpu/Makefile" 2>/dev/null
export PATH="$PKT/scratch/bin:$PATH"
verilator --version
run() { local name=$1; shift; local t0=$(date +%s)
  "$@" > "$PKT/receipts/$name.log" 2>&1; local rc=$?
  echo "$name rc=$rc secs=$(( $(date +%s) - t0 )) :: $(grep -E '^(DL|HZ|TB|D3[A-Z0-9]*|\[build|[0-9]+ checks)' "$PKT/receipts/$name.log" | tail -3 | tr '\n' ' ')"; }
run 10-ucpu-run          make -C "$EXP/tb/ucpu" run
run 11-pp_top-gsi-build  make -C "$EXP/tb/pp_top" gsi-build
run 12-pp_top-deadline   make -C "$EXP/tb/pp_top" deadline
run 13-pp_top-hazards    make -C "$EXP/tb/pp_top" hazards
run 14-pp_top-d3         make -C "$EXP/tb/pp_top" d3
run 15-pp_top-budget     make -C "$EXP/tb/pp_top" budget

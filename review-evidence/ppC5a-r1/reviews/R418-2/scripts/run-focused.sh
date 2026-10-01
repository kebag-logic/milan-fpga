#!/usr/bin/env bash
# Focused lane suites at the exact head, in a disposable git-archive export.
# Usage: run-focused.sh <clone> <head-sha> <packet-dir> <step>
#   step: export | ucpu | pp_top-all | build | deadline | hazards | d3 | budget
set -u
CLONE=$1; HEAD=$2; PKT=$3; STEP=$4
EXP=$PKT/scratch/focused
export PATH="$PKT/scratch/bin:$PATH"
mkdir -p "$PKT/receipts"
run() { local name=$1; shift; local t0; t0=$(date +%s)
  "$@" > "$PKT/receipts/$name.log" 2>&1; local rc=$?
  echo "$name rc=$rc secs=$(( $(date +%s) - t0 )) :: $(grep -E 'checks, [0-9]+ fail' "$PKT/receipts/$name.log" | tail -4 | tr '\n' ' ')"; }
case $STEP in
  export)
    rm -rf "$EXP"; mkdir -p "$EXP"
    git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP"
    # cap the C++ build at 8 jobs (scratch copy only)
    sed -i 's/--build -j 0/--build -j 8/' "$EXP/tb/pp_top/Makefile" "$EXP/tb/ucpu/Makefile"
    verilator --version ;;
  ucpu)       run 10-ucpu-run make -C "$EXP/tb/ucpu" run ;;
  pp_top-all) run 11-pp_top-all make -C "$EXP/tb/pp_top" ;;
  build)      run 12-pp_top-gsi-build make -C "$EXP/tb/pp_top" gsi-build ;;
  deadline)   run 13-pp_top-deadline make -C "$EXP/tb/pp_top" deadline ;;
  hazards)    run 14-pp_top-hazards make -C "$EXP/tb/pp_top" hazards ;;
  d3)         run 15-pp_top-d3 make -C "$EXP/tb/pp_top" d3 ;;
  budget)     run 16-pp_top-budget make -C "$EXP/tb/pp_top" budget ;;
  *) echo "unknown step $STEP"; exit 2 ;;
esac

#!/bin/sh
# R276-5 reviewer probe: build the randomized KL_media_clock_restart property
# check against the head engine and against planted engines, run each over
# a seed range in both modes, and print one verdict line per engine.
# Usage: run.sh <tree> <workdir> [seeds] [cycles]
#   <tree>    a checkout of the head under review (read only)
#   <workdir> a disposable build directory
# Needs VERILATOR on PATH (the pinned 5.050) and python3.
set -eu
TREE=$(cd "$1" && pwd)
WORK=$2
SEEDS=${3:-40}
CYCLES=${4:-200000}
HERE=$(cd "$(dirname "$0")" && pwd)
RTL=$TREE/hdl/ieee1722/avtp/KL_media_clock_restart.sv
mkdir -p "$WORK"
WORK=$(cd "$WORK" && pwd)

python3 "$HERE/plant.py" "$RTL" "$WORK/engines"

overall=0
for eng in "$WORK"/engines/*.sv; do
  name=$(basename "$eng" .sv)
  mdir=$WORK/obj_$name
  verilator --cc --exe --build -j 4 -Wno-fatal -Wno-lint -Wno-style \
    --top-module mcr_prop_top --Mdir "$mdir" -o Vmcr_prop \
    -CFLAGS "-std=c++17 -O2" \
    "$eng" "$HERE/mcr_prop_top.sv" "$HERE/mcr_prop.cpp" >"$WORK/build_$name.log" 2>&1
  fails=0; runs=0
  : >"$WORK/run_$name.log"
  for mode in 0 1; do
    s=1
    while [ "$s" -le "$SEEDS" ]; do
      runs=$((runs + 1))
      if ! "$mdir/Vmcr_prop" "$s" "$CYCLES" "$mode" >>"$WORK/run_$name.log" 2>&1; then
        fails=$((fails + 1))
      fi
      s=$((s + 1))
    done
  done
  sum=$(grep '^seed=' "$WORK/run_$name.log" | awk '
    { for (i = 1; i <= NF; i++) { split($i, kv, "="); v[kv[1]] += kv[2] } }
    END { printf "requests=%d toggles=%d merged=%d residue=%d spurious=%d hold_viol=%d left_pending=%d",
          v["requests"], v["toggles"], v["merged_requests"], v["residue_requests"],
          v["spurious"], v["hold_viol"], v["left_pending"] }')
  echo "ENGINE $name: $fails of $runs runs failed; $sum"
  case $name in
    head) [ "$fails" -eq 0 ] || overall=1 ;;
    *)    [ "$fails" -gt 0 ] || { echo "  ^ SURVIVED: the probe cannot see this engine's defect"; overall=1; } ;;
  esac
done
exit $overall

#!/usr/bin/env bash
# Build and run milan_dp's split leg (default 1x1, one interface) in a clone; optionally then build the head's
# 8x8 two-interface split top. usage: split_leg.sh <clone> <out dir> <verilator> <jobs> [8x8]
set -uo pipefail
clone=$1; out=$2; V=$3; jobs=$4; extra=${5:-}
mkdir -p "$out"
cd "$clone/tb/verilator/milan_dp"
start=$(date +%s)
make VERILATOR="$V" VERILATOR_JOBS="$jobs" -n build-split SPLIT_MDIR="$out/obj_split" > "$out/build-split.n" 2>&1
make VERILATOR="$V" VERILATOR_JOBS="$jobs" build-split SPLIT_MDIR="$out/obj_split" > "$out/build-split.log" 2>&1; echo $? > "$out/build-split.rc"
"$out/obj_split/Vmilan_dp_split" > "$out/split.out" 2>&1; echo $? > "$out/split.rc"
echo "1x1 wall $(( $(date +%s) - start )) s" > "$out/wall.txt"
if [ "$extra" = 8x8 ]; then
  start=$(date +%s)
  make VERILATOR="$V" VERILATOR_JOBS="$jobs" -n build-split SPLIT_MDIR="$out/obj_split8" SPLIT_SHAPE=endstation_ax7101_8x8 SPLIT_STREAMS=8 SPLIT_IF=2 > "$out/build-split8.n" 2>&1
  make VERILATOR="$V" VERILATOR_JOBS="$jobs" build-split SPLIT_MDIR="$out/obj_split8" SPLIT_SHAPE=endstation_ax7101_8x8 SPLIT_STREAMS=8 SPLIT_IF=2 > "$out/build-split8.log" 2>&1; echo $? > "$out/build-split8.rc"
  echo "8x8 wall $(( $(date +%s) - start )) s" >> "$out/wall.txt"
fi
echo done > "$out/DONE"

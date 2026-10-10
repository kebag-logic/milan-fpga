#!/usr/bin/env bash
# Usage: run_liveness_probe.sh <head-checkout> <packet-dir> <verilator> <generator.py>...
# Builds the disposable probe beside the head's real-counter model and runs
# it with 3 and 4 unanswered requests for each generator (ROM) given.
set -u
H=$1; P=$2; V=$3; shift 3
W=$P/scratch/work/liveness; mkdir -p "$W"
D=$H/gptp-processor/hdl
"$V" --cc --exe --build -j 4 --top-module gptp_plane_wrap --Mdir "$W/obj" -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GCLK_HZ_P=8000000 -GPHC_INCR_P=2097152000 -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I$H/tb/common" \
  "$H/tb/verilator/gptp_plane/gptp_plane_wrap.sv" "$H/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
  "$D/ucpu/gptp_ucpu_pkg.sv" "$D/ucpu/KL_gptp_ucpu.sv" "$D/wire/KL_gptp_rx_parser.sv" \
  "$D/wire/KL_gptp_tx_slot.sv" "$D/common/KL_gptp_timer.sv" "$D/top/KL_gptp_engine.sv" \
  "$P/scripts/sim_phc_liveness_probe.cpp" -o probe > "$W/build.log" 2>&1 || { echo BUILD FAILED; exit 2; }
for g in "$@"; do
  n=$(basename "$g" .py); mkdir -p "$W/$n"
  ( cd "$W/$n" && python3 -I "$g" --clk-hz 8000000 -o gptp_ucode.hex > generate.log 2>&1 ) || { echo "$n: generation failed"; continue; }
  for k in 3 4; do
    ( cd "$W/$n" && "$W/obj/probe" $k > run$k.log 2>&1; echo "rc=$?" >> run$k.log )
    echo "$n skips=$k: $(grep -E '^PROBE' "$W/$n/run$k.log") $(grep -c '\[FAIL\]' "$W/$n/run$k.log") FAIL lines, $(tail -1 "$W/$n/run$k.log")"
    grep '\[FAIL\]' "$W/$n/run$k.log" | sed 's/^/    /'
  done
done

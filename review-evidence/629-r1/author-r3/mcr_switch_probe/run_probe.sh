#!/bin/sh
# Builds the probe in a scratch directory with the pinned simulator and runs
# every case. Usage: run_probe.sh <lane checkout> <scratch dir>
set -e
LANE=$1; S=$2
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
mkdir -p "$S"; cp "$(dirname "$0")/sim_switch.cpp" "$S/"; cd "$S"
"$V" --version
sha256sum "$LANE/hdl/ieee1722/avtp/KL_media_clock_restart.sv"
"$V" --cc --exe --build -O3 -j 8 --top-module KL_media_clock_restart \
  -GN_TALKERS_P=2 "$LANE/hdl/ieee1722/avtp/KL_media_clock_restart.sv" \
  sim_switch.cpp -o sim_switch > build.log 2>&1
echo "build rc=0"
echo "== scaled clock: A = 100 cycles per AAF PDU, C = 1,600; every switch phase across one CRF period"
./obj_dir/sim_switch 100 40 4000 1 1 design late disruption era_fall
./obj_dir/sim_switch 100 40 4000 8 1 first_pdu
./obj_dir/sim_switch 100 90 4000 1 1 design late era_fall
echo "== real clock: 100 MHz (milan_datapath.sv:67), A = 12,500 cycles (125 us), C = 200,000 (2 ms); L = 5 ms; 32 phases across one CRF period"
./obj_dir/sim_switch 12500 40 500000 6257 1 design late disruption era_fall
./obj_dir/sim_switch 12500 2000 500000 6257 1 design late era_fall
./obj_dir/sim_switch 12500 40 500000 6257 1250 first_pdu

#!/bin/sh
# Run one probe copy's gptp_shadow suite (`make run`) with the given Verilator.
# Usage: run_probe.sh <probe-dir> <verilator> <log> <rc-file>
dir=$1; vl=$2; log=$3; rcf=$4
cd "$dir/tb/verilator/gptp_shadow" || { echo 2 > "$rcf"; exit 2; }
make run VERILATOR="$vl" VERILATOR_JOBS=2 > "$log" 2>&1
echo $? > "$rcf"

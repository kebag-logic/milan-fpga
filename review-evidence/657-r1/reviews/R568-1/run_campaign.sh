#!/bin/sh
# Usage: run_campaign.sh <clone> <receipt-dir> <shim-bin-dir>
# Runs the exact acceptance command with the pinned compiler on CPUs 0-11.
set -u
clone=$1; out=$2; bin=$3
export PATH="$bin:$PATH" VERILATOR="$bin/verilator" VERILATOR_JOBS=6
cd "$clone" || exit 99
{ verilator --version; git rev-parse HEAD; date -u +%FT%TZ; } > "$out/campaign.env"
start=$(date +%s.%N)
taskset -c 0-11 make -C tb/verilator/milan_dp_render tdm8render-mutants > "$out/campaign.log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "rc=$rc elapsed=$(echo "$end - $start" | bc)" > "$out/campaign.rc"

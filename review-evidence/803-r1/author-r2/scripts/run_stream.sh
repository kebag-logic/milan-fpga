#!/usr/bin/env bash
# run_stream.sh <clone> <out> <jobs> <args...>: one mutant stream of round2_mutants.py under the lane environment.
set -uo pipefail
clone=$1; out=$2; jobs=$3; shift 3
source $MANAGEMENT/2026-09-23/803-a693b/scripts/env.sh
export VERILATOR_JOBS=$jobs
mkdir -p "$out"
date -u +%FT%TZ > "$out/start"
python3 -I $MANAGEMENT/2026-09-23/803-a693b/scripts/round2_mutants.py "$clone" "$out" "$@" > "$out/stream.out" 2>&1
echo $? > "$out/stream.rc"
date -u +%FT%TZ > "$out/end"

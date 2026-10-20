#!/usr/bin/env bash
# Focused exact-head suites and gates, each in the background with its own
# log, rc and wall seconds; waits for all before returning.
# usage: focused.sh <tree> <receipts-dir> <verilator>
set -uo pipefail
tree=$1; out=$2; V=$3
mkdir -p "$out"
export PATH="$(cd "$(dirname "$0")/.." && pwd)/scratch/bin:$PATH"; verilator --version > "$out/verilator-version.txt"
job() { # name dir cmd...
  local name=$1 dir=$2; shift 2
  ( s=$(date +%s); cd "$dir" && "$@" > "$out/$name.log" 2>&1; rc=$?
    echo $rc > "$out/$name.rc"; echo $(( $(date +%s) - s )) > "$out/$name.secs" ) &
}
job pp_top        "$tree/tb/pp_top"        make VERILATOR="$V"
job acmp_listener "$tree/tb/acmp_listener" make VERILATOR="$V"
job acmp_nvm      "$tree/tb/acmp_nvm"      make VERILATOR="$V"
job aecp_cmds     "$tree/tb/aecp_cmds"     make VERILATOR="$V"
job timer_map     "$tree/tb/timer_map"     make VERILATOR="$V"
job ucpu          "$tree/tb/ucpu"          make VERILATOR="$V"
job upc_map       "$tree"                  python3 scripts/check_upc_map.py
job gen_matrix    "$tree"                  python3 scripts/gen_matrix.py --check
job make_check    "$tree"                  make check
job lint_hdl      "$tree"                  bash scripts/lint_hdl.sh
wait

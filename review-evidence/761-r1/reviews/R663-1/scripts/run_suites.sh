#!/usr/bin/env bash
# Launch the focused suites for the reviewed head in a copy of its tree.
# Usage: run_suites.sh <src_tree> <log_dir> <bin_dir_with_pinned_verilator>
# Each job writes <name>.log and <name>.rc (rc=N) into <log_dir>; jobs run
# detached and CPU-pinned so the total stays within 16 cores.
set -u
SRC=$1; LOGS=$2; BIN=$3
mkdir -p "$LOGS"
export PATH="$BIN:$PATH" VERILATOR="$BIN/verilator"
job() {  # name cpus dir cmd...
  local name=$1 cpus=$2 dir=$3; shift 3
  ( cd "$SRC/$dir" && date -Is > "$LOGS/$name.start"
    taskset -c "$cpus" "$@" > "$LOGS/$name.log" 2>&1
    echo "rc=$?" > "$LOGS/$name.rc"; date -Is > "$LOGS/$name.end" ) &
}
job crf_rx      0-3  tb/verilator/crf_rx      make
job avtp_rxmon  4-7  tb/verilator/avtp_rxmon  make
job mclk        8-15 tb/verilator/milan_dp_mclk env SIM_JOBS=8 make VERILATOR_JOBS=8
job lint        0-1  .                        python3 scripts/lint_rtl.py --check
wait

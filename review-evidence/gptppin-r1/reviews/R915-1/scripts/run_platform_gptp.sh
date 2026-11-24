#!/usr/bin/env bash
# Run the platform-level gPTP consumer suites in one probe tree.
# Usage: run_platform_gptp.sh <tree-root> <log-dir> <verilator>
# Each job writes <log-dir>/<job>.log and <log-dir>/<job>.rc; jobs run
# concurrently and this script returns when all are started.
set -u
tree=$1 logs=$2 vl=$3
mkdir -p "$logs"
export MAKEFLAGS=--no-print-directory
job() {
  local name=$1; shift
  ( cd "$tree" && "$@" ) > "$logs/$name.log" 2>&1
  echo $? > "$logs/$name.rc"
}
tb=tb/verilator
job gptp_shadow  make -C $tb/gptp_shadow  run VERILATOR="$vl" VERILATOR_JOBS=4 &
job gptp_plane   make -C $tb/gptp_plane   all VERILATOR="$vl" &
job gptp_tables  make -C $tb/gptp_tables  run VERILATOR="$vl" &
job gptp_txts    make -C $tb/gptp_txts    run VERILATOR="$vl" &
job milan_dp_gptp_legs bash -c "make -C $tb/milan_dp gptp VERILATOR='$vl' && make -C $tb/milan_dp gptp-lat VERILATOR='$vl'" &
wait
echo ALL-DONE > "$logs/ALL.done"

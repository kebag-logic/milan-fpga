#!/usr/bin/env bash
# Runs the PR's two focused suites at the checked-out head, concurrently,
# with the given Verilator first on PATH. Usage:
#   run_focused_suites.sh <checkout> <receipt-dir> <verilator-dir>
set -u
repo=$1; out=$2; vdir=$3
mkdir -p "$out"
export PATH="$vdir:$PATH"
verilator --version > "$out/verilator_version.txt" 2>&1
for suite in milan_dp_gm_steps gptp_plane; do
  ( cd "$repo/tb/verilator/$suite" && /usr/bin/time -v make -j8 > "$out/$suite.log" 2>&1; echo $? > "$out/$suite.rc" ) &
done
wait

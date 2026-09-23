#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Run a built sim_nxn leg from the tree's milan_dp directory (the hex images
# are read relative to it) and print a one-line receipt:
#   leg=<leg> exit=<rc> checks=<n> failures=<n> ok_lines=<n> fail_lines=<n>
#   crf_ok=<n> crf_fail=<n> wall_s=<s> bin_sha256=<sha>
# crf_* count the [CTRS-CRF] and [NOTIFY-CRF] check lines. The full log goes
# to <log>.
# usage: run_leg.sh <tree> <leg> <mdir> <log>
set -u
tree=$1; leg=$2; mdir=$3; log=$4
bin="$mdir/Vmilan_dp_$leg"
cd "$tree/tb/verilator/milan_dp" || exit 2
t0=$(date +%s)
"$bin" > "$log" 2>&1
rc=$?
t1=$(date +%s)
tally=$(grep -E '^checks: [0-9]+ +failures: [0-9]+' "$log" | tail -1)
checks=$(echo "$tally" | awk '{print $2}')
failures=$(echo "$tally" | awk '{print $4}')
okl=$(grep -c '^  \[ok\]' "$log")
fl=$(grep -c '^  \[FAIL\]' "$log")
cok=$(grep -cE '^  \[ok\]   \[(CTRS|NOTIFY)-CRF\]' "$log")
cfl=$(grep -cE '^  \[FAIL\] \[(CTRS|NOTIFY)-CRF\]' "$log")
sha=$(sha256sum "$bin" | cut -d' ' -f1)
echo "leg=$leg exit=$rc checks=${checks:-none} failures=${failures:-none} ok_lines=$okl fail_lines=$fl crf_ok=$cok crf_fail=$cfl wall_s=$((t1 - t0)) bin_sha256=$sha"

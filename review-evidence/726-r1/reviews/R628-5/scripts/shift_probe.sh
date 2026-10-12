#!/bin/bash
# Re-run a built #726 fixture with COUNTERS_WINDOW_SHIFT=<cycles>; print verdict and gap summary.
# usage: shift_probe.sh <work-dir> <shift-cycles> <out.log>
w=$1; s=$2; out=$3
cd "$w/tb/verilator/milan_dp" && COUNTERS_WINDOW_SHIFT=$s "$w/obj/stream_counters" > "$out" 2>&1
echo "rc=$?" >> "$out"

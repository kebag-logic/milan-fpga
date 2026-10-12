#!/bin/sh
# Re-run an already-built clean stream-counter model with COUNTERS_WINDOW_SHIFT
# (cycles; 1000 cycles = 1 simulated ms) and keep its log.
# Usage: shift_probe.sh <work-dir> <shift> <out-log>
cd "$1/tb/verilator/milan_dp" || exit 2
COUNTERS_WINDOW_SHIFT=$2 "$1/obj/stream_counters" > "$3" 2>&1

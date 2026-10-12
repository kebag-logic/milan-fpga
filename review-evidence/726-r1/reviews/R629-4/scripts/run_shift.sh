#!/bin/sh
# Usage: run_shift.sh WORK SHIFT_CYCLES OUTLOG : rerun a built fixture with the window grid shifted
W=$1; cd "$W/tb/verilator/milan_dp" || exit 2
COUNTERS_WINDOW_SHIFT=$2 "$W/obj/stream_counters" > "$3" 2>&1; echo "rc=$?" >> "$3"

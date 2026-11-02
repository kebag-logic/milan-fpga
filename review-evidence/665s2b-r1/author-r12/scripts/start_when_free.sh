#!/bin/bash
# Start a unit on the next free 16-CPU range (cpu_ranges.py pick), retrying until one is free.
# usage: start_when_free.sh NAME SCRIPT ARG...
set -u
N=$1; shift
S=$MANAGEMENT/2026-09-23
while :; do
    R=$(python3 $S/cpu_ranges.py pick)
    if [ -n "$R" ]; then
        exec $S/665s2b-a683o/scripts/unit.sh "$N" "$R" 8G -- "$@"
    fi
    python3 -c 'import time; time.sleep(30)'
done

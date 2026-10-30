#!/bin/bash
# launch.sh <first> <last> <log>: run gate steps detached
cd $LANES/797-r1-regref || exit 2
exec python3 /tmp/797-a711-tools/run_gates.py $LANES/797-r1-regref $MANAGEMENT/2026-09-23/797-a711/receipts/gates "$1" "$2" > "$3" 2>&1

#!/bin/bash
# Waits for the go file (no heavy job of this lane running), then takes the exclusive Vivado lock.
M=<scratch>
export TMPDIR="$M/tmp" PYTHONDONTWRITEBYTECODE=1
while [ ! -f "$M/vivado.go" ]; do sleep 10; done
date -Is > "$M/vivado-queued.txt"
flock $VIVADO_LOCK bash -c 'date -Is > "$0/vivado-acquired.txt"; python3 "$0/vivado_bank.py" 0df486370990fddf9b60096be2f2371150692a10' "$M" > "$M/vivado-bank.log" 2>&1
rc=$?
echo "$rc" > "$M/vivado-bank.rc"
date -Is > "$M/vivado-finished.txt"
exit "$rc"

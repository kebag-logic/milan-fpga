#!/bin/sh
# The sweep with one added SRP state (receipts/patches/sweep_mode8.diff):
# mode 8 = a poll answered, then a STRMW_CTRL write whose write is not yet
# answered. m6 = head RTL (want rc 0: the page's words hold); m7 = the m4 RTL
# mutant, STRMW_CTRL-write clear removed (want rc 1: the added state kills it).
# Usage: run_mode8.sh <packet-dir>
set -u
P=$1; S=$P/scratch; R=$P/receipts
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
for m in m6 m7; do
  ( python3 -I "$S/$m/scripts/register_read_sweep.py" --work "$S/w/$m" > "$R/sweep_mode8_$m.log" 2>&1; echo $? > "$R/sweep_mode8_$m.rc" ) &
done
wait
for m in m6 m7; do echo "sweep_mode8_$m rc=$(cat "$R/sweep_mode8_$m.rc")"; tail -1 "$R/sweep_mode8_$m.log"; done

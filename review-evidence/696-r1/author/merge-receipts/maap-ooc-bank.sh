#!/bin/bash
# Starts after the measurement job has ended (no other Vivado or heavy job of this lane), under the exclusive lock.
M=<scratch>
export TMPDIR="$M/tmp" PYTHONDONTWRITEBYTECODE=1
while [ ! -f "$M/vivado-bank.rc" ]; do sleep 10; done
flock $VIVADO_LOCK bash -c 'date -Is > "$0/maap-ooc-acquired.txt"; python3 "$0/maap_ooc_bank.py"' "$M" > "$M/maap-ooc-bank.log" 2>&1
rc=$?
echo "$rc" > "$M/maap-ooc-bank.rc"
exit "$rc"

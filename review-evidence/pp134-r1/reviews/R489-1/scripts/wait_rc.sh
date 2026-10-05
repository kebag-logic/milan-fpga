#!/bin/bash
# Wait (up to $2 seconds, default 540) for every named rc file under $1.
# Usage: wait_rc.sh <receipts-dir> <seconds> name...
R=$1; T=${2:-540}; shift 2
end=$((SECONDS + T))
while [ $SECONDS -lt $end ]; do
  missing=0
  for n in "$@"; do [ -f "$R/$n.rc" ] || missing=$((missing + 1)); done
  [ $missing -eq 0 ] && break
  sleep 10
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$R/$n.rc" 2>/dev/null || echo PENDING)"; done

#!/bin/sh
# Wait (up to N seconds) until every named rc file exists; print each rc.
# Usage: wait_rc.sh <receipts dir> <seconds> <name...>
R=$1; T=$2; shift 2; i=0
while [ $i -lt "$T" ]; do
  missing=0; for n in "$@"; do [ -f "$R/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break; sleep 5; i=$((i+5))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$R/$n.rc" 2>/dev/null || echo PENDING)"; done

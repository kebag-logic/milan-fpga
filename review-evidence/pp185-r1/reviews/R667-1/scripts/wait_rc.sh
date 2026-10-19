#!/usr/bin/env bash
# Wait (at most MAXS seconds, default 540) until every named job has an rc file.
# usage: wait_rc.sh NAME...
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
max=${MAXS:-540}; t=0
while :; do
  missing=0
  for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break
  [ $t -ge $max ] && { echo "still running after ${t}s"; break; }
  sleep 10; t=$((t + 10))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$PKT/receipts/$n.rc" 2>/dev/null || echo pending)"; done

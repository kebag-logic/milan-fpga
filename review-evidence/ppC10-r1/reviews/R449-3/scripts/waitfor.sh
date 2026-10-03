#!/usr/bin/env bash
# Wait (at most <secs>) until every named job has an rc file; print status.
# usage: waitfor.sh <secs> <name...>
P="${PACKET_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
secs=$1; shift
end=$(( $(date +%s) + secs ))
while :; do
  done_all=1
  for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || done_all=0; done
  [ "$done_all" -eq 1 ] && break
  [ "$(date +%s)" -ge "$end" ] && break
  sleep 10
done
for n in "$@"; do
  if [ -f "$P/receipts/$n.rc" ]; then echo "$n rc=$(cat "$P/receipts/$n.rc") wall=$(cat "$P/receipts/$n.time" 2>/dev/null)s"
  else echo "$n RUNNING ($(wc -l < "$P/receipts/$n.log" 2>/dev/null) log lines)"; fi
done

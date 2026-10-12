#!/usr/bin/env bash
# Wait (bounded) until every named campaign has an rc file; print the rcs.
# usage: wait.sh SECONDS NAME...
P=$(cd "$(dirname "$0")/.." && pwd)
limit=$1; shift
end=$(( $(date +%s) + limit ))
while :; do
  missing=0
  for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || missing=1; done
  [ $missing -eq 0 ] && break
  [ "$(date +%s)" -ge $end ] && break
  sleep 10
done
for n in "$@"; do
  if [ -f "$P/receipts/$n.rc" ]; then echo "$n rc=$(cat "$P/receipts/$n.rc")"; else echo "$n RUNNING"; fi
done

#!/bin/sh
# Poll for rc files of the named jobs, up to LIMIT seconds (default 540).
# usage: wait.sh NAME...
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
LIMIT=${LIMIT:-540}
t=0
while :; do
  left=0
  for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || left=$((left+1)); done
  [ $left -eq 0 ] && break
  [ $t -ge "$LIMIT" ] && break
  sleep 15; t=$((t+15))
done
for n in "$@"; do
  if [ -f "$PKT/receipts/$n.rc" ]; then echo "$n rc=$(cat "$PKT/receipts/$n.rc")"
  else echo "$n RUNNING: $(tail -c 200 "$PKT/receipts/$n.log" | tr '\n' ' ')"; fi
done

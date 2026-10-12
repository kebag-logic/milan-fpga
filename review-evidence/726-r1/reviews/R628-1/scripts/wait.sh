#!/bin/sh
# Usage: wait.sh <seconds> <name...>
# Polls receipts/<name>.rc for up to <seconds>; prints each status.
PKT=$(cd "$(dirname "$0")/.." && pwd)
limit=$1; shift
t=0
while :; do
  done_all=1
  for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break
  [ $t -ge "$limit" ] && break
  sleep 10; t=$((t+10))
done
for n in "$@"; do
  if [ -f "$PKT/receipts/$n.rc" ]; then echo "$n rc=$(cat "$PKT/receipts/$n.rc")"
  else echo "$n RUNNING"; fi
done
free -g | sed -n 2p

#!/bin/sh
# Usage: wait.sh MAXSEC NAME...   Polls until all NAME.rc exist or MAXSEC elapses; prints status
P=$REVIEWS/726-r628-3-packet/receipts
max=$1; shift; t=0
while [ $t -lt $max ]; do
  done=1; for n in "$@"; do [ -f $P/$n.rc ] || done=0; done
  [ $done = 1 ] && break
  sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat $P/$n.rc 2>/dev/null || echo RUNNING)"; done
free -g | sed -n 2p

#!/bin/sh
# wait.sh MAXSEC NAME...: poll until every NAME.rc exists or MAXSEC elapses
P=$REVIEWS/665ft-r506-2-packet
max=$1; shift; t=0
while [ $t -lt $max ]; do
  done=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || done=0; done
  [ $done = 1 ] && break; sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat $P/receipts/$n.rc 2>/dev/null || echo PENDING)"; done

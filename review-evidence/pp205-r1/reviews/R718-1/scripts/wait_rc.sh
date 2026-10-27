#!/bin/sh
# wait_rc.sh SECONDS NAME... : poll until every NAME.rc exists or SECONDS pass;
# print each rc (or PENDING)
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
limit=$1; shift
t=0
while [ "$t" -lt "$limit" ]; do
  done_all=1
  for n in "$@"; do [ -f "$PACKET/receipts/$n.rc" ] || done_all=0; done
  [ "$done_all" = 1 ] && break
  sleep 10; t=$((t + 10))
done
for n in "$@"; do
  if [ -f "$PACKET/receipts/$n.rc" ]; then echo "$n rc=$(cat "$PACKET/receipts/$n.rc")"; else echo "$n PENDING"; fi
done

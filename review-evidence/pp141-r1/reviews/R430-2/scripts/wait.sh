#!/bin/sh
# usage: wait.sh SECONDS NAME...  - wait until every NAME.rc exists or SECONDS pass; print status
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
R=$PACKET/receipts
lim=$1; shift; t=0
while [ $t -lt $lim ]; do
  all=1; for n in "$@"; do [ -f $R/$n.rc ] || all=0; done
  [ $all = 1 ] && break
  sleep 15; t=$((t+15))
done
for n in "$@"; do echo "$n rc=$(cat $R/$n.rc 2>/dev/null || echo running) killed=$(grep -c KILLED $R/$n.log) | $(tail -1 $R/$n.log | cut -c1-120)"; done

#!/bin/bash
# wait_rc.sh SECONDS NAME... : wait (bounded) until every NAME.rc exists; print them
P=${P:-$REVIEWS/pp134-r488-3-packet}
lim=$1; shift; end=$(( $(date +%s) + lim ))
while :; do
  missing=0; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break
  [ $(date +%s) -ge $end ] && break
  sleep 10
done
for n in "$@"; do printf '%s: ' "$n"; cat "$P/receipts/$n.rc" 2>/dev/null || echo RUNNING; done

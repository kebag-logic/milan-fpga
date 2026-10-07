#!/bin/bash
# [R530] wait.sh MAXSEC NAME... : wait until every $PACKET/receipts/NAME.rc exists or MAXSEC passes; print status.
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
max=$1; shift; t=0
while :; do done_all=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break; [ $t -ge "$max" ] && break; sleep 10; t=$((t+10)); done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo RUNNING)"; done

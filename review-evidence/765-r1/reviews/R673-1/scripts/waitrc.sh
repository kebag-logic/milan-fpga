#!/bin/bash
# waitrc.sh SECONDS NAME... : poll until every NAME.rc exists or SECONDS elapse
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
lim=$1; shift; t=0
while :; do
  done_all=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break
  [ $t -ge $lim ] && break
  sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%s: %s\n' "$n" "$(cat $P/receipts/$n.rc 2>/dev/null || echo RUNNING)"; done

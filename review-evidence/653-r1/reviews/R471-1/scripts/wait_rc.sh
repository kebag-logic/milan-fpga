#!/bin/sh
# wait_rc.sh SECONDS NAME... - poll until every receipts/NAME.rc exists or SECONDS elapse
P=$(cd "$(dirname "$0")/.." && pwd)
lim=$1; shift; t=0
while [ $t -lt $lim ]; do
  ok=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || ok=0; done
  [ $ok = 1 ] && break
  sleep 15; t=$((t+15))
done
for n in "$@"; do printf '%s: rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo running)"; done

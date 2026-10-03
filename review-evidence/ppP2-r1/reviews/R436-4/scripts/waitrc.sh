#!/usr/bin/env bash
# waitrc.sh MAXSEC NAME... : wait until every receipts/NAME.rc exists or MAXSEC elapses; print rcs
P=$(cd "$(dirname "$0")/.." && pwd)
max=$1; shift; t=0
while :; do
  done_all=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break
  [ $t -ge $max ] && break
  sleep 5; t=$((t+5))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done

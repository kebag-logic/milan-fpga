#!/usr/bin/env bash
# wait_rc.sh SECONDS NAME... : wait until each receipts/NAME.rc exists or SECONDS pass; print status
P="$(cd "$(dirname "$0")/.." && pwd)"
lim=$1; shift; t=0
while :; do
  missing=0; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break; [ $t -ge $lim ] && break
  sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%-28s %s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo RUNNING)"; done

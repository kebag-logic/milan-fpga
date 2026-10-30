#!/bin/sh
# wait_rc.sh SECONDS NAME... : wait up to SECONDS for every NAME.rc, print them
P=$(cd "$(dirname "$0")/.." && pwd)
t=$1; shift; end=$(( $(date +%s) + t ))
while [ "$(date +%s)" -lt "$end" ]; do
  all=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || all=0; done
  [ $all = 1 ] && break; sleep 10
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done

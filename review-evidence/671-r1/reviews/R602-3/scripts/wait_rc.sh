#!/bin/sh
# wait_rc.sh SECONDS NAME... : wait up to SECONDS for every receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd)
t=$1; shift
end=$(( $(date +%s) + t ))
while [ "$(date +%s)" -lt "$end" ]; do
  ok=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || ok=0; done
  [ $ok = 1 ] && break; sleep 5
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done

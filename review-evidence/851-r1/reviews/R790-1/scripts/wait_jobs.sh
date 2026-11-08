#!/usr/bin/env bash
# wait_jobs.sh SECONDS NAME... : wait up to SECONDS for receipts/NAME.rc to exist
t=$1; shift; out="$(cd "$(dirname "$0")/.." && pwd)/receipts"
end=$(( $(date +%s) + t ))
while :; do
  missing=0; for n in "$@"; do [ -f "$out/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break
  [ $(date +%s) -ge $end ] && break
  read -t 15 < /dev/zero 2>/dev/null || true
  python3 -c 'import time; time.sleep(15)'
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$out/$n.rc" 2>/dev/null || echo PENDING)"; done

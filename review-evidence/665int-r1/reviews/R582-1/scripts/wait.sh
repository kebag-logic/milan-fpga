#!/usr/bin/env bash
# wait.sh SECONDS NAME... : poll until every NAME.rc exists or SECONDS pass; print status
R="$(cd "$(dirname "$0")/.." && pwd)/receipts"
end=$(( $(date +%s) + $1 )); shift
while :; do
  missing=0; for n in "$@"; do [ -f "$R/$n.rc" ] || missing=1; done
  [ $missing = 0 ] && break
  [ $(date +%s) -ge $end ] && break
  read -t 15 _ < /dev/zero 2>/dev/null || true; timeout 15 tail -f /dev/null 2>/dev/null
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat $R/$n.rc 2>/dev/null || echo RUNNING)"; done

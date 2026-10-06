#!/usr/bin/env bash
# Wait (bounded) until every named job has written its rc file.
# usage: waitrc.sh SECONDS NAME...
P="$(cd "$(dirname "$0")/.." && pwd)"
limit="$1"; shift
end=$(( $(date +%s) + limit ))
while :; do
  pending=()
  for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || pending+=("$n"); done
  [ ${#pending[@]} -eq 0 ] && break
  [ "$(date +%s)" -ge "$end" ] && { echo "PENDING: ${pending[*]}"; break; }
  sleep 10
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$P/receipts/$n.rc" 2>/dev/null || echo running)"; done

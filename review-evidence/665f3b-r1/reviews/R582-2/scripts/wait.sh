#!/usr/bin/env bash
# Wait (at most LIMIT seconds) until every named run has an rc file; print status.
# Usage: wait.sh LIMIT NAME...
limit="$1"; shift
runs="$(cd "$(dirname "$0")/.." && pwd)/runs"
end=$((SECONDS + limit))
while :; do
  pending=0
  for n in "$@"; do [ -f "$runs/$n.rc" ] || pending=$((pending + 1)); done
  [ "$pending" -eq 0 ] && break
  [ "$SECONDS" -ge "$end" ] && break
  read -r -t 10 < /dev/zero 2>/dev/null || true
  sleep 10 2>/dev/null || true
done
for n in "$@"; do
  if [ -f "$runs/$n.rc" ]; then echo "$n rc=$(cat "$runs/$n.rc")"; else echo "$n RUNNING ($(wc -l < "$runs/$n.log") log lines)"; fi
done

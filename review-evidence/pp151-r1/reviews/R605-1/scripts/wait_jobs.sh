#!/usr/bin/env bash
# Wait (at most <secs>) for every named job's rc file; print each status.
# usage: wait_jobs.sh <secs> <name...>
K=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
limit=$1; shift
end=$(( $(date +%s) + limit ))
while :; do
  pending=()
  for n in "$@"; do [ -f "$K/receipts/$n.rc" ] || pending+=("$n"); done
  [ ${#pending[@]} -eq 0 ] && break
  [ "$(date +%s)" -ge "$end" ] && break
  sleep 10
done
for n in "$@"; do
  if [ -f "$K/receipts/$n.rc" ]; then
    echo "$n rc=$(cat "$K/receipts/$n.rc") secs=$(cat "$K/receipts/$n.secs") :: $(tail -1 "$K/receipts/$n.log")"
  else
    echo "$n PENDING :: $(tail -1 "$K/receipts/$n.log" 2>/dev/null)"
  fi
done
free -g | awk 'NR==2{print "mem used " $3 " GiB, available " $7 " GiB"}'

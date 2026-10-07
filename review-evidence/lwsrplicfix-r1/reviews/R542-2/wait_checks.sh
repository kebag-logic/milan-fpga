#!/usr/bin/env bash
# Poll receipts/head until every launched job has an rc file, for at most N seconds.
# Usage: wait_checks.sh <packet> [seconds]
PKT=${1:?packet}
LIMIT=${2:-540}
OUT="$PKT/receipts/head"
end=$((SECONDS + LIMIT))
while :; do
    pending=0
    for log in "$OUT"/*.log; do
        [ -e "${log%.log}.rc" ] || pending=$((pending + 1))
    done
    [ "$pending" -eq 0 ] && break
    [ "$SECONDS" -ge "$end" ] && break
    sleep 5
done
for log in "$OUT"/*.log; do
    n=$(basename "$log" .log)
    printf '%-28s rc=%s\n' "$n" "$(cat "${log%.log}.rc" 2>/dev/null || echo PENDING)"
done
echo "pending=$pending"

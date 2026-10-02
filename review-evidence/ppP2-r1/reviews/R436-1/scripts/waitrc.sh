#!/usr/bin/env bash
# waitrc.sh MAXSEC NAME... : wait (foreground) until every receipts/NAME.rc exists or MAXSEC passes
PKT=$(cd "$(dirname "$0")/.." && pwd)
max=$1; shift; t=0
while :; do
  pending=""; for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || pending="$pending $n"; done
  [ -z "$pending" ] && break
  [ "$t" -ge "$max" ] && { echo "still pending:$pending"; exit 1; }
  sleep 10; t=$((t+10))
done
for n in "$@"; do echo "$n rc=$(cat "$PKT/receipts/$n.rc")"; done

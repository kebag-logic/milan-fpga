#!/usr/bin/env bash
# wait.sh <seconds> <name...>: poll receipts/<name>.rc until all exist or the time is up
P="$(cd "$(dirname "$0")/.." && pwd)"; lim=$1; shift; t=0
while :; do left=0; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || left=$((left+1)); done
  [ $left -eq 0 ] && break; [ $t -ge $lim ] && { echo "still running: $left"; break; }; sleep 10; t=$((t+10)); done
for n in "$@"; do printf '%-34s rc=%s secs=%s\n' "$n" "$(cat $P/receipts/$n.rc 2>/dev/null || echo -)" "$(cat $P/receipts/$n.secs 2>/dev/null || echo -)"; done

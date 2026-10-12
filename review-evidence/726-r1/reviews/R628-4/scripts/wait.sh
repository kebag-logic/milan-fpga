#!/bin/sh
# Usage: wait.sh <max_seconds> <name...>; polls logs/<name>.rc in the foreground
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
max=$1; shift; t=0
while [ $t -lt $max ]; do
  done_all=1; for n in "$@"; do [ -f "$P/logs/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break
  sleep 15; t=$((t+15))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat $P/logs/$n.rc 2>/dev/null || echo PENDING)"; done
free -g | sed -n 2p

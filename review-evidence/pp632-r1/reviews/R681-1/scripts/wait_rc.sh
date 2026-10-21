#!/usr/bin/env bash
# Wait (at most MAXSEC, default 540) for every named campaign's rc file; print status.
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
MAXSEC=${MAXSEC:-540}
end=$(( $(date +%s) + MAXSEC ))
while :; do
  pending=0
  for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || pending=1; done
  [ $pending = 0 ] && break
  [ "$(date +%s)" -ge "$end" ] && break
  python3 -c 'import time; time.sleep(15)'
done
for n in "$@"; do
  if [ -f "$PKT/receipts/$n.rc" ]; then echo "$n rc=$(cat $PKT/receipts/$n.rc) $(cat $PKT/receipts/$n.wall 2>/dev/null)"; else echo "$n RUNNING ($(wc -l <$PKT/receipts/$n.log) log lines)"; fi
done
free -g | head -2

#!/bin/sh
# usage: wait.sh MAXSEC NAME...   (polls receipts/NAME.rc; prints rc of each; exit 3 if any pending)
set -u
max=$1; shift
t=0
while :; do
  pend=0
  for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || pend=1; done
  [ $pend = 0 ] && break
  [ $t -ge $max ] && break
  sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%-34s %s\n' "$n" "$(cat "$PKT/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done
[ $pend = 0 ] || exit 3

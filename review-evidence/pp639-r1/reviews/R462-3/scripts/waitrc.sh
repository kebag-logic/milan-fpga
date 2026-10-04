#!/bin/sh
# waitrc.sh SECONDS NAME... : wait up to SECONDS for every NAME.rc, then print rcs
PKT=$REVIEWS/pp639-r462-3-packet
lim=$1; shift; t=0
while [ $t -lt $lim ]; do
  done_all=1; for n in "$@"; do [ -f "$PKT/receipts/$n.rc" ] || done_all=0; done
  [ $done_all = 1 ] && break; sleep 10; t=$((t+10))
done
for n in "$@"; do printf '%s rc=%s\n' "$n" "$(cat "$PKT/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done

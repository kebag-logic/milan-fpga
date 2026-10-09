#!/bin/sh
# wait.sh NAME... : wait (max 540 s) for rc files, print them
: "${PACKET:?set PACKET}"
end=$(( $(date +%s) + 540 ))
for n in "$@"; do while [ ! -f "$PACKET/receipts/$n.rc" ] && [ $(date +%s) -lt $end ]; do sleep 5; done; printf '%s rc=%s\n' "$n" "$(cat "$PACKET/receipts/$n.rc" 2>/dev/null || echo PENDING)"; done

#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: wait_rc.sh <seconds> <label...>; waits up to <seconds> for rc files
PKT=$(cd "$(dirname "$0")/.." && pwd)
limit=$1; shift; t=0
for l in "$@"; do
  while [ ! -s "$PKT/receipts/$l.rc" ] && [ $t -lt $limit ]; do sleep 5; t=$((t+5)); done
  printf '%s rc=%s\n' "$l" "$(cat "$PKT/receipts/$l.rc" 2>/dev/null || echo PENDING)"
done

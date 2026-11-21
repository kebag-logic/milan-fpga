#!/bin/sh
# usage: status.sh [lines]; prints each job's rc and its last verdict lines
R=${PACKET:-$REVIEWS/948-r877-1-packet}/receipts
for f in "$R"/*.log; do
  n=$(basename "$f" .log)
  rc=$(cat "$R/$n.rc" 2>/dev/null || echo running)
  echo "== $n rc=$rc"
  grep -aE 'PASS|FAIL|checks|caught|SURVIVED|failures|Error|error:|rc=' "$f" | grep -avE '^g\+\+|Wno-' | tail -n "${1:-4}" | cut -c1-220
done

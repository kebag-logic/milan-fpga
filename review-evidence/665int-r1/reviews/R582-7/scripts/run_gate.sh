#!/usr/bin/env bash
# run_gate.sh NAME CMD... : run CMD from the candidate clone, keep its full
# output in receipts/NAME.log and its exit status, wall time and argv in
# receipts/NAME.rc. Never fails itself, so a batch of gates runs to the end.
set -u
PACKET="$(cd "$(dirname "$0")/.." && pwd)"
CLONE="${CLONE:-$REVIEWS/r582-7-665int}"
name="$1"; shift
log="$PACKET/receipts/$name.log"
rcf="$PACKET/receipts/$name.rc"
t0=$(date +%s)
( cd "$CLONE" && "$@" ) >"$log" 2>&1
rc=$?
t1=$(date +%s)
printf 'rc=%d wall_s=%d head=%s argv=%s\n' "$rc" "$((t1 - t0))" \
  "$(git -C "$CLONE" rev-parse HEAD)" "$*" >"$rcf"
exit 0

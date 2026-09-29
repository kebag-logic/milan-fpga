#!/usr/bin/env bash
# Run one b2_action.py action under the bench lock, with a hard deadline.
# usage: run_action.sh <name> <mode>; endpoints from B2_ENDPOINTS (private, not in the packet).
set -u
. "${B2_ENDPOINTS:?}"
N=$1; M=$2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $N"
timeout -k 10 150 flock -w 60 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); timeout -k 5 130 python3 -B $(dirname "$0")/b2_action.py $N $M $CONSOLE_PORT $CONTROLLER $CTL_IF $TAP_HOST $TAP_IF; echo ACTION_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

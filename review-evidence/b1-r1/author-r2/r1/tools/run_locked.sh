#!/usr/bin/env bash
# Run one b1_action.py action under the bench lock, with a hard deadline.
# usage: run_locked.sh <name> <duration_s> <kind> [HOLD] [PRE]
# Endpoints come from the private file named by B1_ENDPOINTS (not in this packet).
set -u
. "${B1_ENDPOINTS:?}"
N=$1; D=$2; K=$3; H=${4:-20}; PRE=${5:-10}
T=$(( D + 200 ))
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $N"
timeout -k 10 $T flock -w 120 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); python3 -B $(dirname $0)/b1_action.py $N $D $K $CONSOLE_PORT $CONTROLLER $CTL_IF $TAP_HOST $TAP_IF $STRIP_HOST $H $PRE; echo ACTION_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

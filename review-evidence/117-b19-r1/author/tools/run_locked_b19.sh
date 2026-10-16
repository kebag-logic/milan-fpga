#!/usr/bin/env bash
# Lane B19: run one a624_action.py action under the bench lock with a hard deadline
# (lane B1's run_locked.sh with the environment B19_ENV). Endpoints come from B19_ENV (private).
# usage: run_locked_b19.sh <name> <duration_s> <kind> [HOLD] [PRE]
set -u
. "${B19_ENV:?}"
N=$1; D=$2; K=$3; H=${4:-20}; PRE=${5:-10}
T=$(( D + 200 ))
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $N"
timeout -k 10 $T flock -w 120 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); python3 -B $(dirname $0)/a624_action.py $N $D $K $CONSOLE_PORT $CONTROLLER $CTL_IF $TAP_HOST $TAP_IF $STRIP_HOST $H $PRE; echo ACTION_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

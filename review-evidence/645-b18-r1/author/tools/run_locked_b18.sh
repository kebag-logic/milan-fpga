#!/usr/bin/env bash
# Lane B18: run one action under the bench lock with a hard deadline, logging the lock window
# (lane B17's run_locked_b17.sh with the environment B18_ENV).
# usage: run_locked_b17.sh <deadline_s> <command> [args...]; endpoints from B18_ENV (private).
set -u
set -a; . "${B18_ENV:?}"; set +a
DL=$1; shift
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ)"
timeout -k 10 $((DL + 80)) flock -w 60 /tmp/milan-bench.lock bash -c '
DL=$0
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout -k 10 "$DL" "$@"
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$DL" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

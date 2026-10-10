#!/usr/bin/env bash
# Run one run_b6.py case under the bench lock, with a hard deadline (lane B5's run_locked.sh,
# retargeted). usage: run_locked.sh <packet_dir> <limit_s> <name> <case> <window_s>
# Raw files go to /tmp/b6-a477/raw/<name>; endpoints come from B6_ENV (private).
set -u
. "${B6_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0
python3 -B "$P/tools/run_b6.py" "$@" /tmp/b6-a477/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

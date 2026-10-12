#!/usr/bin/env bash
# Run one run_b7.py case under the bench lock, with a hard deadline (lane B6's run_locked.sh,
# retargeted: the environment B7_ENV, the tool run_b7.py, raw files under /tmp/b7-a519/raw).
# usage: run_locked_b7.sh <packet_dir> <limit_s> <name> <case> <window_s>
set -u
. "${B7_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0
python3 -B "$P/tools/run_b7.py" "$@" /tmp/b7-a519/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

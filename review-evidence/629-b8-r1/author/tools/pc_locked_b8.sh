#!/usr/bin/env bash
# Run one pc_b8.py stage under the bench lock with a hard deadline (run_locked_b8.sh's pattern).
# usage: pc_locked_b8.sh <packet_dir> <limit_s> <name> pre|post
set -u
. "${B8_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0
python3 -B "$P/tools/pc_b8.py" "$@"
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

#!/usr/bin/env bash
# Run one run_*.py action under the bench lock, with a hard deadline (lane B3's run_locked.sh,
# retargeted). usage: run_locked.sh <packet_dir> <tool> <limit_s> <args...>
# Raw files go to /tmp/b5-a472/raw/<name>; endpoints come from B5_ENV (private).
set -u
. "${B5_ENV:?}"
P=$1; TOOL=$2; LIM=$3; shift 3
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 10 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0; T=$1; shift 1
python3 -B "$P/tools/$T" "$@" /tmp/b5-a472/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$TOOL" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

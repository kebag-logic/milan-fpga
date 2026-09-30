#!/usr/bin/env bash
# Run one run_*.py action under the bench lock, with a hard deadline.
# usage: run_locked.sh <packet_dir> <tool> <name> <seconds_a> <seconds_b> <limit_s>
# Raw files go to /tmp/b3-a453/raw/<name>; endpoints come from B3_ENV (private).
set -u
. "${B3_ENV:?}"
P=$1; TOOL=$2; N=$3; A=$4; B=$5; LIM=$6
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $N"
timeout -k 10 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
python3 -B "$0/tools/$1" "$2" "$3" "$4" /tmp/b3-a453/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$TOOL" "$N" "$A" "$B"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

#!/usr/bin/env bash
# Lane B10 copy of lane B9's run_locked_b9.sh: only the environment name (B10_ENV), the controller staging (/tmp/a534), the board files (/tmp/a534-*), the raw root (/tmp/b10-a534/raw) and the private directory (B10_PRIV) differ; any other change is stated below this line.
# Lane B9 copy of lane B8's run_locked_b8.sh: the environment B10_ENV, the tool run_b10.py and the
# raw root /tmp/b10-a534/raw differ, and the lock is taken with flock -o so no process of the case
# inherits the lock's descriptor.
# Run one run_b10.py case under the bench lock, with a hard deadline.
# usage: run_locked_b9.sh <packet_dir> <limit_s> <name> <case> <window_s>
set -u
. "${B10_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -o -w 20 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0
python3 -B "$P/tools/run_b10.py" "$@" /tmp/b10-a534/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

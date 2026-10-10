#!/usr/bin/env bash
# Lane B8 copy of lane B7's script: only the environment name (B8_ENV), the controller staging (/tmp/a521), the controller tool name (b8_ctl.py) and the raw root (/tmp/b8-a521/raw) differ.
# Run one run_b8.py case under the bench lock, with a hard deadline (lane B6's run_locked.sh,
# retargeted: the environment B8_ENV, the tool run_b8.py, raw files under /tmp/b8-a521/raw).
# usage: run_locked_b7.sh <packet_dir> <limit_s> <name> <case> <window_s>
set -u
. "${B8_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0
python3 -B "$P/tools/run_b8.py" "$@" /tmp/b8-a521/raw
echo "ACTION_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

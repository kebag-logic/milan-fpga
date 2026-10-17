#!/usr/bin/env bash
# Lane B21: run one long action under the bench lock as a tracked, detached process with a hard deadline.
# The lock is held by flock for the action only and released when the action or its deadline ends.
# usage: tracked_b21.sh <marker_dir> <limit_s> <command...>
# Writes <marker_dir>/lock.txt (LOCK/UNLOCK/ACTION_RC lines) and <marker_dir>/done when finished.
set -u
M=$1; LIM=$2; shift 2
mkdir -p "$M"; rm -f "$M/done"
setsid nohup bash -c '
M=$0; LIM=$1; shift 2
{ echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ)"
  timeout -k 10 "$LIM" flock -w 120 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); \"\$@\"; echo ACTION_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)" _ "$@"
  echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"; } > "$M/lock.txt" 2>&1
touch "$M/done"' "$M" "$LIM" x "$@" > /dev/null 2>&1 < /dev/null &
echo "LAUNCHED pid=$! $(date -u +%FT%T.%3NZ)"

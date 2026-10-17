#!/usr/bin/env bash
# Lane B21: one SoC board console action under the bench lock, through soccon_b21.py (root prompt only;
# a login prompt aborts with rc 3 and nothing is typed). Lock window lines go to stdout.
# usage: soc_locked_b21.sh <packet_dir> <log_relpath> <timeout_s> '<shell command>'
set -u
. "${B21_ENV:?}"
P=$1; LOG=$2; T=$3; CMD=$4
mkdir -p "$(dirname "$P/$LOG")"
timeout -k 5 $((T + 60)) flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout $(($2 + 30)) python3 -B "$0/tools/soccon_b21.py" "$SOC_CONSOLE" "$0/$1" "$2" "$3" > /dev/null 2>&1
echo "SOC_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$LOG" "$T" "$CMD"
echo "LOCK_RC=$?"

#!/usr/bin/env bash
# Lane B15 (new; lane B10's run_locked_b10.sh pattern): one four-point capture as one locked action
# with a hard deadline. Inside the lock: the SoC board's to-host bridge leg (the one leg running as
# found) is stopped by the PID its `status` names, after the command-line check (soc_legs_b15.sh);
# points_b15.py runs; the leg is restarted with its recorded line, whatever points_b15.py returned.
# The lock is taken with flock -o, so no process of the action inherits the lock's descriptor.
# usage: points_locked_b15.sh <packet_dir> <limit_s> <name> <seconds> [control]
set -u
. "${B15_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -o -w 30 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0; N=$1
mkdir -p "$P/soc"
PID=$(timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$SOC_SSH" "tdm8-uac2.sh status" | sed -n "s/.*to-host: running (pid \([0-9]*\)).*/\1/p")
echo "TO_HOST_PID=$PID"
if [ -z "$PID" ]; then echo "NO_TO_HOST_LEG: nothing stopped"; else "$P/tools/soc_legs_b15.sh" "$P/soc/$N-legs.log" stop to-host "$PID"; echo "STOP_RC=$?"; fi
python3 -B "$P/tools/points_b15.py" "$1" /tmp/b15-a588/raw "$2" ${3:+"$3"}
echo "ACTION_RC=$?"
if [ -n "$PID" ]; then "$P/tools/soc_legs_b15.sh" "$P/soc/$N-legs.log" start to-host; echo "START_RC=$?"; fi
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

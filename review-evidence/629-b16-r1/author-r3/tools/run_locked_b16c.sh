#!/usr/bin/env bash
# Lane B16c copy of lane B16b's run_locked_b16.sh (SHA-256 8694f9b0e3c3...). B16c changes: it runs run_b16c.py; modes
# bcrf and baaf also stop and restart the to-host leg (they record McASP0, as mode b0); the deadline's kill delay is
# 100 s (B16b: 20 s); the deadline runs inside the lock (flock, then timeout; B16b: timeout, then flock), so a
# deadline's SIGTERM reaches the action's process group while flock keeps the lock; the inner shell traps that
# SIGTERM, so that run_b16c.py's teardown (both clock sources and the binds, read back) and the leg's restart both
# finish, under the lock, after a deadline. Lane B16b's header follows, as written.
# Lane B16 (lane B15's points_locked_b15.sh, generalised): one run_b16.py action as one locked action with a
# hard deadline. Inside the lock: for the modes that record McASP0 (dirb, dirbloop) the SoC board's to-host
# bridge leg is stopped by the PID its `status` names, after the command-line check (soc_legs_b16.sh), and
# restarted with its recorded line whatever run_b16.py returned; modes loop and looptap touch no leg. B16b: mode
# dira (lane B15's positive control, McASP0 playing and recording) also stops and restarts the leg; so does mode
# b0 (added to this condition after run b0, whose McASP0 recording found the device busy because the leg was left
# running). The lock is taken
# with flock -o, so no process of the action inherits the lock's descriptor.
# usage: run_locked_b16c.sh <packet_dir> <limit_s> <name> <mode> <seconds>
set -u
. "${B16_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
flock -o -w 30 /tmp/milan-bench.lock timeout -k 100 "$LIM" bash -c '
trap "echo DEADLINE_TERM \$(date -u +%FT%T.%3NZ)" TERM
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0; N=$1; M=$2
mkdir -p "$P/soc"
PID=""
if [ "$M" = dirb ] || [ "$M" = dirbloop ] || [ "$M" = dira ] || [ "$M" = b0 ] || [ "$M" = bcrf ] || [ "$M" = baaf ]; then
  PID=$(timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$SOC_SSH" "tdm8-uac2.sh status" | sed -n "s/.*to-host: running (pid \([0-9]*\)).*/\1/p")
  echo "TO_HOST_PID=$PID"
  if [ -z "$PID" ]; then echo "NO_TO_HOST_LEG: nothing stopped"; else "$P/tools/soc_legs_b16.sh" "$P/soc/$N-legs.log" stop to-host "$PID"; echo "STOP_RC=$?"; fi
fi
python3 -B "$P/tools/run_b16c.py" "$N" /tmp/b16-a603/raw "$M" "$3"
echo "ACTION_RC=$?"
if [ -n "$PID" ]; then "$P/tools/soc_legs_b16.sh" "$P/soc/$N-legs.log" start to-host; echo "START_RC=$?"; fi
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

#!/usr/bin/env bash
# Lane B16 (lane B15's points_locked_b15.sh, generalised): one run_b16.py action as one locked action with a
# hard deadline. Inside the lock: for the modes that record McASP0 (dirb, dirbloop) the SoC board's to-host
# bridge leg is stopped by the PID its `status` names, after the command-line check (soc_legs_b16.sh), and
# restarted with its recorded line whatever run_b16.py returned; modes loop and looptap touch no leg. B16b: mode
# dira (lane B15's positive control, McASP0 playing and recording) also stops and restarts the leg; so does mode
# b0 (added to this condition after run b0, whose McASP0 recording found the device busy because the leg was left
# running). The lock is taken
# with flock -o, so no process of the action inherits the lock's descriptor.
# usage: run_locked_b16.sh <packet_dir> <limit_s> <name> <mode> <seconds>
set -u
. "${B16_ENV:?}"
P=$1; LIM=$2; shift 2
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ) $*"
timeout -k 20 "$LIM" flock -o -w 30 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
P=$0; N=$1; M=$2
mkdir -p "$P/soc"
PID=""
if [ "$M" = dirb ] || [ "$M" = dirbloop ] || [ "$M" = dira ] || [ "$M" = b0 ]; then
  PID=$(timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$SOC_SSH" "tdm8-uac2.sh status" | sed -n "s/.*to-host: running (pid \([0-9]*\)).*/\1/p")
  echo "TO_HOST_PID=$PID"
  if [ -z "$PID" ]; then echo "NO_TO_HOST_LEG: nothing stopped"; else "$P/tools/soc_legs_b16.sh" "$P/soc/$N-legs.log" stop to-host "$PID"; echo "STOP_RC=$?"; fi
fi
python3 -B "$P/tools/run_b16.py" "$N" /tmp/b16-a603/raw "$M" "$3"
echo "ACTION_RC=$?"
if [ -n "$PID" ]; then "$P/tools/soc_legs_b16.sh" "$P/soc/$N-legs.log" start to-host; echo "START_RC=$?"; fi
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$@"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"

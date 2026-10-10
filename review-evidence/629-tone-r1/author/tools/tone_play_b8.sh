#!/usr/bin/env bash
# Lane B8: start, check or stop the Direction B tone on the tone source's
# playback (<tone-source-layout>, b8_tone.py's loop at -20 dBFS),
# under the bench lock. Only playback is started or stopped: no mixer, routing or clock
# setting of the tone source is read or written by any tool here.
#   start <seconds>  writes the loop (b8_tone.py) and starts the playback detached, with its
#                    own log; the playback ends by itself after <seconds>
#   status           the playback's PID and command line, and the tone source's playback status
#   stop             stops the playback by its PID, after checking the command line
# The tone source's card, the playback layout and the log stay in the private directory
# named by B8_ENV's directory (not in this packet). Prints one line per step.
# The lock is taken with flock -o, so the detached playback never inherits the lock's descriptor.
set -u
. "${B8_ENV:?}"
P=$1; OP=$2
PRIV=$(dirname "$B8_ENV")
LOOP=$PRIV/<tone-loop-file>
LOG=$PRIV/<tone-log-file>
LINE="aplay -D hw:<tone-source-card>,0 -t raw -f $PLAY_FMT -r 48000 -c $PLAY_NCH"
find_pid() { for p in $(pgrep -x aplay); do A=$(tr '\0' ' ' < /proc/$p/cmdline); case "$A" in "$LINE -d "*) echo "$p";; esac; done; }
timeout -k 5 120 flock -o -w 120 /tmp/milan-bench.lock bash -c "$(declare -f find_pid); "'
set -u
P=$0; OP=$1; LOOP=$2; LOG=$3; LINE=$4; DUR=${5:-0}
echo "LOCK $(date -u +%FT%T.%3NZ)"
case "$OP" in
start)
  if [ -n "$(find_pid)" ]; then echo "ALREADY_PLAYING $(find_pid)"; exit 3; fi
  python3 -B "$P/tools/b8_tone.py" "$LOOP" > "$LOG.loop" 2>&1 || { echo LOOP_FAILED; exit 4; }
  echo "LOOP_SHA256 $(sha256sum < "$LOOP" | cut -c1-64)"
  setsid nohup bash -c "while cat $LOOP; do :; done | sudo -n $LINE -d $DUR -v; echo aplay_rc=\$?" > "$LOG" 2>&1 < /dev/null &
  sleep 3
  echo "PID $(find_pid)"
  [ -n "$(find_pid)" ] && echo STARTED || { echo START_FAILED; tail -3 "$LOG"; exit 5; }
  ;;
status)
  echo "PID $(find_pid)"
  ;;
stop)
  p=$(find_pid)
  if [ -z "$p" ]; then echo NOT_PLAYING; else sudo -n kill $p && echo "KILLED $p"; fi
  sleep 2
  echo "PID_AFTER $(find_pid)"
  tail -1 "$LOG"
  ;;
esac
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$OP" "$LOOP" "$LOG" "$LINE" "${3:-0}"
echo "LOCK_RC=$?"

#!/usr/bin/env bash
# Lane B9: start, check or stop the Direction B tone on the tone source's playback (b9_tone.py's
# loop at -20 dBFS), under the bench lock. Lane B8's tone_play_b8.sh with two lane B9 changes:
# the tone source's card, playback layout, status file and the private directory come from the
# private environment (TONE_CARD, PLAY_FMT, PLAY_NCH, TONE_PROC, B9_ENV's directory), so this
# file names none of them and needs no mask; and `status` also reads the tone source's playback
# substream status twice, 1 s apart (state and hw_ptr, read from /proc, passive).
# Only playback is started or stopped: no mixer, routing or clock setting of the tone source is
# read or written by any tool here.
#   start <seconds>  writes the loop (b9_tone.py) and starts the playback detached, with its own
#                    log; the playback ends by itself after <seconds>
#   status           the playback's PID and command line, and the substream status
#   stop             stops the playback by its PID, after checking the command line
# The lock is taken with flock -o, so the detached playback never inherits the lock's descriptor.
set -u
. "${B9_ENV:?}"
P=$1; OP=$2
PRIV=$(dirname "$B9_ENV")
LOOP=$PRIV/tone-loop.raw
LOG=$PRIV/tone-play.log
LINE="aplay -D hw:$TONE_CARD,0 -t raw -f $PLAY_FMT -r 48000 -c $PLAY_NCH -B $PLAY_BUF_US"
find_pid() { for p in $(pgrep -x aplay); do A=$(tr '\0' ' ' < /proc/$p/cmdline); case "$A" in "$LINE -d "*) echo "$p";; esac; done; }
timeout -k 5 120 flock -o -w 120 /tmp/milan-bench.lock bash -c "$(declare -f find_pid); "'
set -u
P=$0; OP=$1; LOOP=$2; LOG=$3; LINE=$4; DUR=${5:-0}
echo "LOCK $(date -u +%FT%T.%3NZ)"
st() { for i in 1 2; do echo "STATUS $(date -u +%FT%T.%3NZ) $(grep -E "^(state|hw_ptr|trigger_time)" "$TONE_PROC" 2>/dev/null | tr -s " " | tr "\n" " ")"; [ $i = 1 ] && sleep 1; done; }
case "$OP" in
start)
  if [ -n "$(find_pid)" ]; then echo "ALREADY_PLAYING $(find_pid)"; exit 3; fi
  python3 -B "$P/tools/b9_tone.py" "$LOOP" > "$LOG.loop" 2>&1 || { echo LOOP_FAILED; exit 4; }
  echo "LOOP_SHA256 $(sha256sum < "$LOOP" | cut -c1-64)"
  setsid nohup bash -c "while cat $LOOP; do :; done | sudo -n $LINE -d $DUR -v; echo aplay_rc=\$?" > "$LOG" 2>&1 < /dev/null &
  sleep 3
  echo "PID $(find_pid)"
  [ -n "$(find_pid)" ] && echo STARTED || { echo START_FAILED; tail -3 "$LOG"; exit 5; }
  st
  ;;
status)
  echo "PID $(find_pid)"
  st
  ;;
stop)
  p=$(find_pid)
  if [ -z "$p" ]; then echo NOT_PLAYING; else sudo -n kill $p && echo "KILLED $p"; fi
  sleep 2
  echo "PID_AFTER $(find_pid)"
  tail -1 "$LOG"
  st
  ;;
esac
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$OP" "$LOOP" "$LOG" "$LINE" "${3:-0}"
echo "LOCK_RC=$?"

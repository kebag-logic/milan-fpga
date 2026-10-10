#!/usr/bin/env bash
# Lane B15 copy of lane B10's tone_play_b10.sh. Changes: the environment is B15_ENV and the private
# directory B15_PRIV; `start` and `status` end with a passive read of the tone source's level meters
# (mixer_read_b15.py ... passive: it listens to what the mixer daemon publishes and sends nothing), the
# read-only proof that the playback reaches the outputs that feed the reference peer; its rows go to
# the private directory. Everything else is lane B10's: b9_tone.py's loop at -20 dBFS, the playback
# detached with its own log, ended by itself after <seconds>, stopped by its PID after a command-line
# check. The lock is taken with flock -o, so the detached playback never inherits the lock's descriptor.
# Only playback is started or stopped: no mixer, routing or clock setting of the tone source is written.
# usage: tone_play_b15.sh <packet_dir> start <seconds> | status | stop
set -u
. "${B15_ENV:?}"
P=$1; OP=$2
PRIV=$B15_PRIV
LOOP=$PRIV/tone-loop.raw
LOG=$PRIV/tone-play.log
LINE="aplay -D hw:$TONE_CARD,0 -t raw -f $PLAY_FMT -r 48000 -c $PLAY_NCH -B $PLAY_BUF_US"
find_pid() { for p in $(pgrep -x aplay); do A=$(tr '\0' ' ' < /proc/$p/cmdline); case "$A" in "$LINE -d "*) echo "$p";; esac; done; }
timeout -k 5 120 flock -o -w 120 /tmp/milan-bench.lock bash -c "$(declare -f find_pid); "'
set -u
P=$0; OP=$1; LOOP=$2; LOG=$3; LINE=$4; DUR=${5:-0}
echo "LOCK $(date -u +%FT%T.%3NZ)"
st() { for i in 1 2; do echo "STATUS $(date -u +%FT%T.%3NZ) $(grep -E "^(state|hw_ptr|trigger_time)" "$TONE_PROC" 2>/dev/null | tr -s " " | tr "\n" " ")"; [ $i = 1 ] && sleep 1; done; }
meters() { timeout 20 python3 -I "$P/tools/mixer_read_b15.py" "$B15_PRIV/meters-$1-$(date +%H%M%S).json" 3 passive > "$B15_PRIV/meters-$1.last" 2>&1; echo "METERS_RC=$? (rows private)"; }
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
  meters start
  ;;
status)
  echo "PID $(find_pid)"
  st
  meters status
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

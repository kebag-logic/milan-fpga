#!/bin/bash
# Ctrl-C behaviour: start a driver in its own process group with SIGINT at
# its default disposition (a non-interactive shell's `&` would ignore it),
# wait until mutants are in flight, send SIGINT to the whole group as a
# terminal would, then time the exit (capped), and look for survivors and
# leftover temporary trees.
# usage: probe_interrupt.sh <packet> <name> <cpus> <engine-dir> <delay-s> <cap-s> <cmd...>
set -u
PKT=$1; NAME=$2; CPUS=$3; DIR=$4; DELAY=$5; CAP=$6; shift 6
T=$PKT/scratch/tmp/$NAME; mkdir -p "$T"
OUT=$PKT/receipts/$NAME.log
cd "$DIR"
export PATH="$PKT/scratch/bin:$PATH" TMPDIR="$T"
setsid python3 -I -c 'import os, signal, sys
signal.signal(signal.SIGINT, signal.SIG_DFL)
os.execvp(sys.argv[1], sys.argv[1:])' taskset -c "$CPUS" "$@" \
  > "$PKT/receipts/$NAME.stdout" 2> "$PKT/receipts/$NAME.stderr" &
PID=$!
sleep "$DELAY"
{
echo "driver: $*"
echo "SigIgn of driver: $(awk '/SigIgn/{print $2}' /proc/$PID/status)"
echo "before SIGINT: $(find "$T" -mindepth 2 -maxdepth 2 -type d | wc -l) staged dirs; group procs $(pgrep -g "$PID" | wc -l)"
START=$(date +%s.%N)
kill -INT -- "-$PID"
n=0
while kill -0 "$PID" 2>/dev/null && [ $n -lt $((CAP * 2)) ]; do sleep 0.5; n=$((n + 1)); done
END=$(date +%s.%N)
if kill -0 "$PID" 2>/dev/null; then
  echo "STILL RUNNING $CAP s after SIGINT; group procs $(pgrep -g "$PID" | wc -l)"
  pgrep -g "$PID" -a | cut -c1-160
  pkill -KILL -g "$PID"; wait "$PID" 2>/dev/null
else
  wait "$PID"; echo "rc $?; exit $(echo "$END - $START" | bc) s after SIGINT"
fi
sleep 2
echo "group procs left: $(pgrep -g "$PID" | wc -l)"
echo "temp entries left: $(find "$T" -mindepth 1 | wc -l)"
} > "$OUT" 2>&1
pkill -KILL -g "$PID" 2>/dev/null
cat "$OUT"

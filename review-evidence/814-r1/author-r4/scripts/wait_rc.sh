#!/usr/bin/env bash
# wait_rc.sh <rc-file> [seconds]: poll every 15 s until <rc-file> exists, at most <seconds> (default 540).
set -u
f=$1; lim=${2:-540}; t=0
while [ ! -e "$f" ] && [ "$t" -lt "$lim" ]; do sleep 15; t=$((t + 15)); done
if [ -e "$f" ]; then echo "DONE after ${t}s: $(cat "$f")"; else echo "still running after ${t}s"; fi
grep MemAvailable /proc/meminfo

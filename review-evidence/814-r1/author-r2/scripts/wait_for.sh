#!/usr/bin/env bash
# wait_for.sh <file> <fixed-string> [seconds]: poll every 20 s until <file> contains <fixed-string>, at most
# <seconds> (default 540); prints the file's last lines and the host's MemAvailable either way.
set -u
f=$1; pat=$2; lim=${3:-540}; t=0
while [ "$t" -lt "$lim" ]; do
  grep -qF -- "$pat" "$f" 2>/dev/null && { echo "FOUND after ${t}s"; break; }
  sleep 20; t=$((t + 20))
done
tail -4 "$f"
grep MemAvailable /proc/meminfo

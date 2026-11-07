#!/usr/bin/env bash
# wait_for.sh <file> <fixed-string> [seconds]: poll every 20 s until <file> holds <fixed-string>, at most <seconds>
# (default 560), then print the chain's last lines, the run's last log line and MemAvailable.
set -u
f=$1; pat=$2; lim=${3:-560}; t=0
while [ "$t" -lt "$lim" ]; do
  grep -qF -- "$pat" "$f" 2>/dev/null && { echo "FOUND after ${t}s"; break; }
  sleep 20; t=$((t + 20))
done
tail -4 "$f"
grep MemAvailable /proc/meminfo

#!/usr/bin/env bash
# Record when each capture_coherence leg's verdict line first appears in a suite log.
#   monitor.sh <log> <out> <pid-to-watch>
log=$1; out=$2; pid=$3
declare -A seen
: > "$out"
while kill -0 "$pid" 2>/dev/null; do
  for m in "== capture_coherence: checks" "== capture_coherence_dp: checks" " checks: " ; do
    if [ -z "${seen[$m]:-}" ] && grep -q -- "$m" "$log" 2>/dev/null; then
      seen[$m]=1; echo "$(date +%s.%N) $(grep -m1 -- "$m" "$log")" >> "$out"
    fi
  done
  sleep 1
done
echo "$(date +%s.%N) exit" >> "$out"

#!/bin/bash
# Stop a part's Vsim of a group an extra part of the same leg started earlier (lane 895 round 2), by PID, after
# printing its arguments; only processes whose arguments name this lane's scratch build. usage: dedupe.sh BUILD PART:EXTRA...
set -u
B=/data-2/milan/tmp/895-a775/builds/$1; shift
for pair in "$@"; do
  part=${pair%%:*} extra=${pair##*:}
  for g in $(tr ',' ' ' < $B/part$extra.groups); do
    # the extra part's copy must be running, or its log complete: a copy stopped or not started stops nothing
    if ! pgrep -f -x "$B/native/Vsim $B/results-p$extra/$g.txt -" >/dev/null && \
       ! tail -c 400 "$B/results-p$extra/$g.log" 2>/dev/null | grep -q '^RESULT'; then continue; fi
    for pid in $(pgrep -f -x "$B/native/Vsim $B/results-p$part/$g.txt -"); do
      a=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null)
      case "$a" in "$B/native/Vsim $B/results-p$part/$g.txt - ") echo "$(date +%T) stop $pid: $a"; kill "$pid";; esac
    done
  done
done

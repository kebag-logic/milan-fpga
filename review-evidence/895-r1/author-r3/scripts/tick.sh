#!/bin/bash
# tick.sh: one pass of round 3's starter (lane 895): queued arm A parts first (start_parts.sh on the clone r3/S),
# then the head checks of aux.queue (lines: NAME|CWD|COMMAND; one unit each on a picked range, MemAvailable > 20 GB;
# a started line is removed). Prints what started and the legs' states.
set -u
M=$MANAGEMENT/2026-09-23
S=$M/895-a775/round3/scripts
T=/data-2/milan/tmp/895-a775
CLONE=$T/r3/S bash $S/start_parts.sh $S/parts.queue 2>&1 | grep -v "no free range"
while IFS='|' read -r name cwd cmd; do
  [ -z "${name:-}" ] && continue
  avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo); [ "$avail" -gt 20 ] || break
  R=$(python3 $M/cpu_ranges.py pick) || break
  if bash $S/unit.sh "$name" "$R" 8G "$cwd" -- "$cmd" >/dev/null 2>&1; then
    echo "$(date +%T) started $name on $R"
    grep -v "^$name|" $S/aux.queue > $S/aux.queue.tmp; mv $S/aux.queue.tmp $S/aux.queue
  fi
  sleep 2
done < <(cat $S/aux.queue)
for f in $T/legs/S-*.log; do n=$(basename $f .log); printf "%s:%s " $n "$(cat $T/legs/$n.rc 2>/dev/null || echo run)"; done; echo

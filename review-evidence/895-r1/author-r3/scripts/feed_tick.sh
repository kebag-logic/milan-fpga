#!/bin/bash
# feed_tick.sh MINUTES: for up to MINUTES, once a minute, start queued arm A parts (start_parts.sh) and the two arm B
# legs (Q-B1, Q-B8: answering-ports, group aecp) while ranges are free and MemAvailable is above 20 GB; print the legs'
# states at the end. Lane 895 round 3.
set -u
M=$MANAGEMENT/2026-09-23
S=$M/895-a775/round3/scripts
S1=$M/895-a775/scripts
T=/data-2/milan/tmp/895-a775
N=$T/r3/N
for i in $(seq 1 "$1"); do
  bash $S/start_parts.sh $S/parts.queue 2>&1 | grep started
  for spec in "Q-B1:1x1:answering-ports:aecp" "Q-B8:8x8:answering-ports:aecp"; do
    n=${spec%%:*}
    systemctl --user is-active --quiet "milan-895-a775-r3-leg-$n.service" && continue
    [ -f "$T/legs/$n.rc" ] && continue
    [ -f "$T/r3/started-$n" ] && continue
    avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
    [ "$avail" -gt 20 ] || continue
    R=$(python3 $M/cpu_ranges.py pick) || continue
    bash $S1/unit.sh "r3-leg-$n" "$R" 10G -- "CLONE=$N bash $S1/leg.sh '$spec'" >/dev/null 2>&1 \
      && touch "$T/r3/started-$n" && echo "$(date +%T) started $n on $R"
  done
  [ "$i" -lt "$1" ] && sleep 60
done
echo "queue left: $(wc -l < $S/parts.queue)"
for f in $T/legs/Q-*.log; do n=$(basename $f .log); printf "%s rc=%s; " $n "$(cat $T/legs/$n.rc 2>/dev/null || echo run)"; done; echo

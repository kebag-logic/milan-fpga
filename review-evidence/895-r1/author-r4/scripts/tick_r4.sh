#!/bin/bash
# One pass of round 4's starter (lane 895): the queue's lines in order, each started as its own unit on a range
# cpu_ranges.py picks while MemAvailable is above 20 GB; a started line is removed. Lines:
#   leg NAME:POINT:VARIANT[:GROUPS]      a leg with its build (leg.sh)
#   part BUILD POINT K                   a part of arm A on BUILD's finished build (part.sh), skipped until it is
# Prints what started and every R4 leg's state.
set -u
M=$MANAGEMENT/2026-09-23
S1=$M/895-a775/scripts
S4=$M/895-a775/round4/scripts
T=/data-2/milan/tmp/895-a775
C=${CLONE:-$T/r4/L}
Q=$S4/legs.queue
while read -r kind a b c; do
  [ -z "${kind:-}" ] && continue
  if [ "$kind" = part ]; then
    [ -f "$T/builds/$a/build.json" ] && [ -x "$T/builds/$a/native/Vsim" ] || continue
  fi
  avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo); [ "$avail" -gt 20 ] || { echo "MemAvailable $avail GB"; break; }
  R=$(python3 $M/cpu_ranges.py pick) || break
  if [ "$kind" = leg ]; then
    n=${a%%:*}; cmd="CLONE=$C bash $S1/leg.sh '$a'"; u="leg-$n"; line="leg $a"
  else
    u="part-$a-p$c"; cmd="CLONE=$C bash $S1/part.sh $a $b $c"; line="part $a $b $c"
  fi
  if bash $S4/unit.sh "$u" "$R" 10G $C -- "$cmd" >/dev/null 2>&1; then
    echo "$(date +%T) started $u on $R"
    grep -v -x -F "$line" $Q > $Q.tmp; mv $Q.tmp $Q
  fi
  sleep 3
done < <(cat $Q)
for f in $T/legs/R4-*.log; do [ -f "$f" ] || continue; n=$(basename $f .log); printf "%s:%s " $n "$(cat $T/legs/$n.rc 2>/dev/null || echo run)"; done; echo

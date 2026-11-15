#!/bin/bash
# One pass of round 7B's starter (lane 895): the queue's lines in order, each started as its own unit (MemoryMax 10G)
# while MemAvailable is above 20 GB: on a range cpu_ranges.py picks, or, when pick gives none, on the session pool
# 96-127 (the owner allows single legs there) while fewer than POOL_MOST (default 2) of this round's units run there.
# A started line is removed. Lines:
#   leg NAME:POINT:VARIANT[:GROUPS]      a leg with its build (leg.sh)
#   part BUILD POINT K [VARIANT]         a part of a leg's groups on BUILD's finished build (part.sh), skipped until then
#   legc CLONE NAME:POINT:VARIANT[:GROUPS]  a leg with its build on another clean clone
set -u
M=$MANAGEMENT/2026-09-23
S1=$M/895-a775/scripts
S6=$M/895-a775/round7/scripts
T=/data-2/milan/tmp/895-a775
C=${CLONE:-$T/r7b/L}
Q=$S6/legs7b.queue
POOL=96-127
pool_running() {
  local n=0 u pid
  for u in $(systemctl --user list-units 'milan-895-a775-r7b-*' --no-legend --plain --state=active | awk '{print $1}'); do
    pid=$(systemctl --user show -p MainPID --value "$u")
    [ "$pid" != 0 ] && taskset -cp "$pid" 2>/dev/null | grep -q "$POOL" && n=$((n + 1))
  done
  echo $n
}
while read -r kind a b c d; do
  [ -z "${kind:-}" ] && continue
  if [ "$kind" = part ]; then
    [ -f "$T/builds/$a/build.json" ] && [ -x "$T/builds/$a/native/Vsim" ] || continue
  fi
  avail=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo); [ "$avail" -gt 20 ] || { echo "MemAvailable $avail GB"; break; }
  R=$(python3 $M/cpu_ranges.py pick 2>/dev/null) || R=
  if [ -z "$R" ]; then
    [ "$(pool_running)" -lt "${POOL_MOST:-2}" ] || break
    R=$POOL
  fi
  CW=$C
  if [ "$kind" = leg ]; then
    n=${a%%:*}; cmd="CLONE=$C bash $S1/leg.sh '$a'"; u="leg-$n"; line="leg $a"
  elif [ "$kind" = legc ]; then
    n=${b%%:*}; cmd="CLONE=$a bash $S1/leg.sh '$b'"; u="leg-$n"; line="legc $a $b"; CW=$a
  else
    u="part-$a-p$c"; cmd="CLONE=$C bash $S1/part.sh $a $b $c ${d:-none}"; line="part $a $b $c${d:+ $d}"
  fi
  if bash $S6/unit_r7b.sh "$u" "$R" 10G $CW -- "$cmd" >/dev/null 2>&1; then
    echo "$(date +%T) started $u on $R"
    grep -v -x -F "$line" $Q > $Q.tmp; mv $Q.tmp $Q
  fi
  sleep 3
done < <(cat $Q)
for f in $T/legs/R7B-*.log; do [ -f "$f" ] || continue; n=$(basename $f .log); printf "%s:%s " $n "$(cat $T/legs/$n.rc 2>/dev/null || echo run)"; done; echo

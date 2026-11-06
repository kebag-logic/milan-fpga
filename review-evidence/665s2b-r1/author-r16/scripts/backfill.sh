#!/bin/bash
# Inside this lane's own unit (112-127): start each queued leg once at most THRESHOLD of the unit's simulations run,
# so its CPUs stay busy as the 8x8 legs' tails end: split legs (leg_split.sh) and plain ones (leg.sh).
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
running() { local n=0; for p in $(pgrep -f "/native/Vsim "); do a=$(taskset -cp $p 2>/dev/null | awk -F': ' '{print $2}'); [ "$a" = "112-127" ] && n=$((n+1)); done; echo $n; }
start() {
    local leg=$1 ck=$2 point=$3 lj=$4 rj=$5 plan=$6; shift 6
    mapfile -t P < "$plan"
    echo "$(date +%T) start $leg (running $(running))" >> $T/logs/backfill.txt
    setsid nohup bash $S/leg_split.sh "$leg" "$ck" "$point" "$lj" "${P[0]}" "$rj" "${P[1]}" "$@" > $T/logs/$leg-driver.out 2>&1 < /dev/null &
    sleep 120
}
plain() {
    local leg=$1 ck=$2 point=$3 jobs=$4 groups=$5; shift 5
    echo "$(date +%T) start $leg (running $(running))" >> $T/logs/backfill.txt
    JOBS=$jobs setsid nohup bash $S/leg.sh "$T/$ck" "$leg" "$point" "$groups" "$@" > $T/logs/$leg-driver.out 2>&1 < /dev/null &
    sleep 120
}
wait_room() { until [ "$(running)" -le "$1" ]; do sleep 60; done; }
wait_room 8; start D-A1 CD 1x1 2 6 $T/plan-D-A1.txt
wait_room 8; start D-B1 CD 1x1 2 6 $T/plan-D-B1.txt --variant answering-ports
wait_room 8; plain AH-A8 C 8x8 8 all --mutation store-step-aged-heavier
wait_room 12; plain P81-A8 CP 8x8-1if 4 backlog,backlog-adp,backlog-adp-refill,backlog-owed
echo "$(date +%T) queue empty" >> $T/logs/backfill.txt

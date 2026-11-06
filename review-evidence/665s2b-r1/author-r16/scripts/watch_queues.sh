#!/bin/bash
# Stop each first-round queue once its first leg has ended, so its second leg, already running as a parallel unit
# (parallel.sh), is not run twice. The queue's own log line records the first leg's end before the second starts.
T=$VALIDATION_STORAGE/665s2b-a683u
declare -A FIRST=([q1]=N-A8 [q2]=N-B8 [q3]=D-A8 [q4]=N-A1)
while :; do
    left=0
    for q in q1 q2 q3 q4; do
        unit=milan-665s2b-a683u-$q
        systemctl --user is-active --quiet "$unit" || continue
        left=1
        if grep -q " end ${FIRST[$q]} " "$T/logs/queue-$q.txt" 2>/dev/null; then
            echo "$(date +%T) stop $unit after ${FIRST[$q]}: $(grep " end ${FIRST[$q]} " "$T/logs/queue-$q.txt")" >> "$T/logs/watch.txt"
            systemctl --user stop "$unit"
        fi
    done
    [ $left = 0 ] && { echo "$(date +%T) done" >> "$T/logs/watch.txt"; exit 0; }
    sleep 5
done

#!/bin/bash
# Run legs one after another: each item is NAME:CHECKOUT:POINT:GROUPS[:extra run.py args]; JOBS from the caller.
# usage: queue.sh LANE ITEM...
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
lane=$1; shift
for item in "$@"; do
    IFS=: read -r name checkout point groups extra <<< "$item"
    echo "$(date +%H:%M:%S) start $name" >> $T/logs/queue-$lane.txt
    # shellcheck disable=SC2086
    $S/leg.sh "$T/$checkout" "$name" "$point" "$groups" $extra
    echo "$(date +%H:%M:%S) end $name $(tail -1 $T/logs/$name.log)" >> $T/logs/queue-$lane.txt
done
echo "$(date +%H:%M:%S) done" >> $T/logs/queue-$lane.txt

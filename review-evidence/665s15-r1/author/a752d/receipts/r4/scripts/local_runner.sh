#!/bin/bash
# Run queued jobs one at a time on this lane's own booked CPUs, popping the shared queue under its lock.
# usage: local_runner.sh QUEUE_FILE
set -u
T=$SCRATCH
Q=$1
source $T/scripts/env.sh
pop() { ( flock 9; head -1 "$Q"; sed -i 1d "$Q" ) 9> "$Q.lock"; }
while true; do
    line=$(pop)
    [ -z "$line" ] && { echo "$(date +%T) local: $(basename $Q) empty" >> $T/logs/gq.txt; exit 0; }
    IFS='|' read -r name mem cmd <<< "$line"
    echo "$(date +%T) $name local on $(taskset -cp $$ | awk -F': ' '{print $2}'): $cmd" >> $T/logs/gq.txt
    /bin/bash -c "$cmd"
    echo "$(date +%T) $name local done rc=$?" >> $T/logs/gq.txt
done

#!/bin/bash
# This lane's own unit (16 CPUs): the 1x1 legs one after another at JOBS from the caller, beside N-A8's save-second.
# usage: ownq.sh   (N-B1h on N-B1's build, then D-A1 and D-B1 on their own builds)
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
q() { echo "$(date +%T) $*" >> $T/logs/queue-own.txt; }
q start N-B1h; $S/leg2.sh $T/C N-B1h N-B1 1x1 "$(cat $T/h-N-B1.groups)" --variant answering-ports; q end N-B1h "$(tail -1 $T/logs/N-B1h.log)"
q start D-A1; $S/leg.sh $T/CD D-A1 1x1 "$(cat $T/sub2.groups)"; q end D-A1 "$(tail -1 $T/logs/D-A1.log)"
q start D-B1; $S/leg.sh $T/CD D-B1 1x1 "$(cat $T/sub2.groups)" --variant answering-ports; q end D-B1 "$(tail -1 $T/logs/D-B1.log)"
q done

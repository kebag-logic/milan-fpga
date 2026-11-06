#!/bin/bash
# This lane's own unit, beside N-A8's save-second and the 1x1 queue: once D-NT8 ends, the small 8x8 legs (the new
# control, 8x8/1if's backlog windows, the planted heavier aged step), then the retry-ageless controls.
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
q() { echo "$(date +%T) $*" >> $T/logs/queue-own2.txt; }
until grep -q "^rc=" $T/logs/D-NT8.log 2>/dev/null; do sleep 30; done
q end D-NT8 "$(tail -1 $T/logs/D-NT8.log)"
q start TB-8; $S/leg.sh $T/C TB-8 8x8 all --variant answering-later --mutation transmit-beside-records; q end TB-8 "$(tail -1 $T/logs/TB-8.log)"
q start P81-A8; $S/leg.sh $T/CP P81-A8 8x8-1if backlog,backlog-adp,backlog-adp-refill,backlog-owed; q end P81-A8 "$(tail -1 $T/logs/P81-A8.log)"
q start AH-A8; $S/leg.sh $T/C AH-A8 8x8 "$(cat $T/ah.groups)" --mutation store-step-aged-heavier; q end AH-A8 "$(tail -1 $T/logs/AH-A8.log)"
q start RA-8; $S/leg.sh $T/C RA-8 8x8 all --variant answering-later --mutation retry-ageless; q end RA-8 "$(tail -1 $T/logs/RA-8.log)"
q start RA-1; $S/leg.sh $T/C RA-1 1x1 all --variant answering-later --mutation retry-ageless; q end RA-1 "$(tail -1 $T/logs/RA-1.log)"
q done

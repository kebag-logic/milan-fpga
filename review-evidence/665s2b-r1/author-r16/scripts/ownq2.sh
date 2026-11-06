#!/bin/bash
# This lane's own unit: the drafts' notice row at 8x8, then the retry-ageless controls at both points.
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
q() { echo "$(date +%T) $*" >> $T/logs/queue-own2.txt; }
q start D-NT8; $S/leg.sh $T/CD D-NT8 8x8 all --variant answering-later; q end D-NT8 "$(tail -1 $T/logs/D-NT8.log)"
q start RA-8; $S/leg.sh $T/C RA-8 8x8 all --variant answering-later --mutation retry-ageless; q end RA-8 "$(tail -1 $T/logs/RA-8.log)"
q start RA-1; $S/leg.sh $T/C RA-1 1x1 all --variant answering-later --mutation retry-ageless; q end RA-1 "$(tail -1 $T/logs/RA-1.log)"
q done

#!/bin/bash
# This lane's own unit (112-127): once RA-1 ends, the drafts' notice rows, 8 jobs each (queue.sh).
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
until grep -q "^rc=" $T/logs/RA-1.log 2>/dev/null; do sleep 30; done
JOBS=8 bash $S/queue.sh u2 "D-NT8:CD:8x8:all:--variant answering-later" "D-NT1:CD:1x1:all:--variant answering-later"

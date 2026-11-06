#!/bin/bash
# This lane's own unit (112-127): once NT-8 ends, the small legs one after another, 8 jobs each (queue.sh).
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
until grep -q "^rc=" $T/logs/NT-8.log 2>/dev/null; do sleep 60; done
JOBS=8 bash $S/queue.sh u "RA-8:C:8x8:all:--variant answering-later --mutation retry-ageless" "RA-1:C:1x1:all:--variant answering-later --mutation retry-ageless" "D-NT8:CD:8x8:all:--variant answering-later" "D-NT1:CD:1x1:all:--variant answering-later" "AH-A8:C:8x8:backlog-adp@verify-aged2-0,backlog-adp@verify-aged2-1,backlog-adp@verify-aged2-2,backlog-adp@verify-aged2-3,backlog-adp@verify-aged2-4,backlog-adp@verify-aged2-5,backlog-adp@verify-aged2-6,backlog-adp@verify-aged2-7:--mutation store-step-aged-heavier" "P81-A8:CP:8x8-1if:backlog,backlog-adp,backlog-adp-refill,backlog-owed"

#!/bin/bash
# Round 15's legs at the code head bf1196b2, four queues of 8 jobs on two booked ranges, on clean clones C (the head)
# and CD (both drafts staged). usage: queues.sh N
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
SUB=backlog,backlog-adp,backlog-adp-refill,backlog-owed,backlog-adp@blank-0,backlog-adp@blank-1,backlog-adp@blank-2,backlog-adp@blank-3,backlog-adp@blank-4,backlog-adp@blank-5,backlog-adp@blank-6,backlog-adp@blank-7,backlog-adp@program-0,backlog-adp@program-1,backlog-adp@program-2,backlog-adp@program-3,backlog-adp@program-4,backlog-adp@program-5,backlog-adp@program-6,backlog-adp@program-7,backlog-adp@verify-0,backlog-adp@verify-1,backlog-adp@verify-2,backlog-adp@verify-3,backlog-adp@verify-4,backlog-adp@verify-5,backlog-adp@verify-6,backlog-adp@verify-7,backlog-adp@blank-aged2-0,backlog-adp@blank-aged2-1,backlog-adp@blank-aged2-2,backlog-adp@blank-aged2-3,backlog-adp@blank-aged2-4,backlog-adp@blank-aged2-5,backlog-adp@blank-aged2-6,backlog-adp@blank-aged2-7,backlog-adp@program-aged2-0,backlog-adp@program-aged2-1,backlog-adp@program-aged2-2,backlog-adp@program-aged2-3,backlog-adp@program-aged2-4,backlog-adp@program-aged2-5,backlog-adp@program-aged2-6,backlog-adp@program-aged2-7,backlog-adp@verify-aged2-0,backlog-adp@verify-aged2-1,backlog-adp@verify-aged2-2,backlog-adp@verify-aged2-3,backlog-adp@verify-aged2-4,backlog-adp@verify-aged2-5,backlog-adp@verify-aged2-6,backlog-adp@verify-aged2-7,save,save-held,save-starved
case "$1" in
1) JOBS=8 $S/queue.sh q1 "N-A8:C:8x8:all" "D-B1:CD:1x1:$SUB,save-second:--variant answering-ports" ;;
2) JOBS=8 $S/queue.sh q2 "N-B8:C:8x8:$SUB:--variant answering-ports" "D-A1:CD:1x1:$SUB,save-second" ;;
3) JOBS=8 $S/queue.sh q3 "D-A8:CD:8x8:$SUB" "N-B1:C:1x1:$SUB,save-second:--variant answering-ports" ;;
4) JOBS=8 $S/queue.sh q4 "N-A1:C:1x1:all" "D-B8:CD:8x8:$SUB:--variant answering-ports" "AH-A8:C:8x8:backlog-adp@verify-aged2-0,backlog-adp@verify-aged2-1,backlog-adp@verify-aged2-2,backlog-adp@verify-aged2-3,backlog-adp@verify-aged2-4,backlog-adp@verify-aged2-5,backlog-adp@verify-aged2-6,backlog-adp@verify-aged2-7:--mutation store-step-aged-heavier" ;;
esac

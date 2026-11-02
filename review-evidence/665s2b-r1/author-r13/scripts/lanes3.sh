#!/bin/bash
T=$VALIDATION_STORAGE/665s2b-a683p; S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts
until grep -q '^rc=' $T/logs/N-A1.log 2>/dev/null; do sleep 30; done
$S/queue.sh 2 "N-B1:C1:1x1:backlog,backlog-adp,backlog-adp-refill,backlog-owed,backlog-adp@blank-0,backlog-adp@blank-1,backlog-adp@blank-2,backlog-adp@blank-3,backlog-adp@blank-4,backlog-adp@blank-5,backlog-adp@blank-6,backlog-adp@blank-7,backlog-adp@program-0,backlog-adp@program-1,backlog-adp@program-2,backlog-adp@program-3,backlog-adp@program-4,backlog-adp@program-5,backlog-adp@program-6,backlog-adp@program-7,backlog-adp@verify-0,backlog-adp@verify-1,backlog-adp@verify-2,backlog-adp@verify-3,backlog-adp@verify-4,backlog-adp@verify-5,backlog-adp@verify-6,backlog-adp@verify-7,save:--variant answering-ports"

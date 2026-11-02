#!/bin/bash
# A save's 24 windows at 8x8, arm A, measurement only: the clone CR prints every pass that ran the flash port.
S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts; T=$VALIDATION_STORAGE/665s2b-a683p
JOBS=16 $S/leg.sh $T/CR R-W8 8x8 "backlog-adp@blank-0,backlog-adp@blank-1,backlog-adp@blank-2,backlog-adp@blank-3,backlog-adp@blank-4,backlog-adp@blank-5,backlog-adp@blank-6,backlog-adp@blank-7,backlog-adp@program-0,backlog-adp@program-1,backlog-adp@program-2,backlog-adp@program-3,backlog-adp@program-4,backlog-adp@program-5,backlog-adp@program-6,backlog-adp@program-7,backlog-adp@verify-0,backlog-adp@verify-1,backlog-adp@verify-2,backlog-adp@verify-3,backlog-adp@verify-4,backlog-adp@verify-5,backlog-adp@verify-6,backlog-adp@verify-7"

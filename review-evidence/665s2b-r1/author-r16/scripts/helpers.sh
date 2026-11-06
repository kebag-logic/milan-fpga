#!/bin/bash
# Helper runs on running legs' builds for their last not-started groups (unstarted.py), each leg later combined with
# its helper by run.py --regrade. usage: helpers.sh N
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
case "$1" in
1) JOBS=16 $S/leg2.sh $T/C N-A8h N-A8 8x8 "$(cat $T/helper-N-A8h.groups)" ;;
2) JOBS=10 $S/leg2.sh $T/CD D-B8h D-B8p 8x8 "$(cat $T/helper-D-B8h.groups)" --variant answering-ports ;;
3) JOBS=6 $S/leg2.sh $T/C N-B1h N-B1p 1x1 "$(cat $T/helper-N-B1h.groups)" --variant answering-ports ;;
esac
case "$1" in
4) JOBS=8 $S/leg2.sh $T/CD D-B1h D-B1p 1x1 "$(cat $T/helper-D-B1h.groups)" --variant answering-ports ;;
5) JOBS=8 $S/leg2.sh $T/CD D-A1h D-A1p 1x1 "$(cat $T/helper-D-A1h.groups)" ;;
esac
case "$1" in
6) JOBS=12 $S/leg2.sh $T/C N-A8h2 N-A8 8x8 "$(cat $T/helper-N-A8h2.only)" ;;
esac
case "$1" in
7) JOBS=8 $S/leg.sh $T/C AH-A8 8x8 backlog-adp@verify-aged2-0,backlog-adp@verify-aged2-1,backlog-adp@verify-aged2-2,backlog-adp@verify-aged2-3,backlog-adp@verify-aged2-4,backlog-adp@verify-aged2-5,backlog-adp@verify-aged2-6,backlog-adp@verify-aged2-7 --mutation store-step-aged-heavier ;;
esac
case "$1" in
8) JOBS=2 $S/leg2.sh $T/C REPRO-A8 N-A8 8x8 backlog-adp@blank-aged1-7,backlog-adp@blank-7 ;;
esac

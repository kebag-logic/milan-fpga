#!/bin/bash
# lanes.sh: the reviewer's measurement runs at the head in two serial lanes run side by side,
# 7 group jobs and 7 make jobs each (make capped by the shim), every run with its own log and rc.
P=$REVIEWS/665s2-r703-2-packet
B=$P/scratch/builds J=$P/scripts/job.sh
G=acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed
lane1() {
  $J a1x1 7 --point 1x1 --build-dir $B/a1x1 --reuse-build --record-budget-findings --jobs 7
  $J s1x1 7 --point 1x1 --build-dir $B/s1x1 --variant shutdown-entry --record-budget-findings --jobs 7
  $J c-slow 7 --point 1x1 --build-dir $B/c-slow --mutation slow-adp-rx --jobs 7
  $J c-slowsd 7 --point 1x1 --build-dir $B/c-slowsd --variant shutdown-entry --mutation slow-adp-shutdown --jobs 7
  $J c-asbuilt 7 --point 1x1 --build-dir $B/c-asbuilt --cpu-regions as-built --jobs 7
  $J b1x1 7 --point 1x1 --build-dir $B/b1x1 --variant answering-ports --groups $G --record-budget-findings --jobs 7
  echo done > $P/scratch/logs/LANE1.done
}
lane2() {
  $J a8x8 7 --point 8x8 --build-dir $B/a8x8 --record-budget-findings --jobs 7
  $J s8x8 7 --point 8x8 --build-dir $B/s8x8 --variant shutdown-entry --record-budget-findings --jobs 7
  $J b8x8 7 --point 8x8 --build-dir $B/b8x8 --variant answering-ports --groups $G --record-budget-findings --jobs 7
  echo done > $P/scratch/logs/LANE2.done
}
lane1 & lane2 & wait

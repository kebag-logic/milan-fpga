#!/bin/bash
# smoke-all.sh: E on 0-3 and F on 4-7 (the booking 0-7), each in its own clone of the WIP tree
T=/data-2/milan/tmp/cicd-a839/r5/tools
$T/piece_smoke.sh E 0-3 follow_ring__1 media_phase__2 &
$T/piece_smoke.sh F 4-7 follow_ring__0 media_phase__0 media_phase__1 &
wait

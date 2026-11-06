#!/bin/bash
# D-A1 and D-B1 side by side in one booked unit, eight jobs each.
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts; T=$VALIDATION_STORAGE/665s2b-a683u
mapfile -t DA1 < $T/plan-D-A1.txt; mapfile -t DB1 < $T/plan-D-B1.txt
bash $S/leg_split.sh D-A1 CD 1x1 2 "${DA1[0]}" 6 "${DA1[1]}" &
bash $S/leg_split.sh D-B1 CD 1x1 2 "${DB1[0]}" 6 "${DB1[1]}" --variant answering-ports &
wait

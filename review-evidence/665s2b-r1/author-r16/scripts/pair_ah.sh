#!/bin/bash
# AH-A8 (the heavier aged step's control) and P81-A8 (section 14's 8x8/1if point) side by side in one booked unit.
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts; T=$VALIDATION_STORAGE/665s2b-a683u
JOBS=8 bash $S/leg.sh $T/C AH-A8 8x8 all --mutation store-step-aged-heavier &
JOBS=4 bash $S/leg.sh $T/CP P81-A8 8x8-1if backlog,backlog-adp,backlog-adp-refill,backlog-owed &
wait

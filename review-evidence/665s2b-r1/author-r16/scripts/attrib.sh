#!/bin/bash
# Three attribution legs at 8x8 (pre-checks, never results), side by side on one booked range: the retried notice's
# groups 0, 1, 4 and 5 on 65251a2f's firmware (X1), with one registration an interface (X2), and with AECP's first
# burst one refill period late as save-starved stages it (X3).
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
JOBS=4 bash $S/leg.sh $VALIDATION_STORAGE/665s2b-a683u/X1 X1-8 8x8 notice-retried-0,notice-retried-1,notice-retried-4,notice-retried-5 --variant answering-later &
JOBS=4 bash $S/leg.sh $VALIDATION_STORAGE/665s2b-a683u/X2 X2-8 8x8 notice-retried-0,notice-retried-1,notice-retried-4,notice-retried-5 --variant answering-later &
JOBS=4 bash $S/leg.sh $VALIDATION_STORAGE/665s2b-a683u/X3 X3-8 8x8 notice-retried-0,notice-retried-1,notice-retried-4,notice-retried-5 --variant answering-later &
wait

#!/bin/bash
# The firmware self-test's four shards at the STOP head, two at a time, each on its own clean clone (fwshard.sh).
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
bash $S/fwshard.sh 555131fa0d409def04432748ad4f569e2f22b5e7 0 & bash $S/fwshard.sh 555131fa0d409def04432748ad4f569e2f22b5e7 1 & wait
bash $S/fwshard.sh 555131fa0d409def04432748ad4f569e2f22b5e7 2 & bash $S/fwshard.sh 555131fa0d409def04432748ad4f569e2f22b5e7 3 & wait
echo done > $VALIDATION_STORAGE/665s2b-a683u/logs/fwstop.done

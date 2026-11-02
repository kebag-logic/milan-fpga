#!/bin/bash
# One final-head shard: as fwshard.sh, the log kept under its own name so the earlier run's stays.
set -u
H=$1 K=$2
T=$VALIDATION_STORAGE/665s2b-a683o
$MANAGEMENT/2026-09-23/665s2b-a683o/scripts/fwshard.sh "$H" "$K"
mv "$T/logs/fwshard-$K.log" "$T/logs/fwfinal-$K.log"

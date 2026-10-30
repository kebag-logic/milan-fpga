#!/bin/sh
# One long run of lane S4 round 3, in the gate environment (env.sh): job.sh NAME COMMAND...
# Runs from the checkout; writes $SCRATCH/NAME.log and $SCRATCH/NAME.rc (the command's exit status).
. $MANAGEMENT/2026-09-23/665s4-a698c/scripts/env.sh
name=$1; shift
cd $LANES/665-s4-f1-target || exit 2
rm -f "$SCRATCH/$name.rc"
PATH="$GATE_BUILDER_PATH:$PATH" "$@" > "$SCRATCH/$name.log" 2>&1
echo $? > "$SCRATCH/$name.rc"

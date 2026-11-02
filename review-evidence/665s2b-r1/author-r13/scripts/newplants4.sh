#!/bin/bash
# The new plants on the lane's working tree (a pre-check, not a gate), named ones only.
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/np4; mkdir -p $TMPDIR
L=$LANES/665-s2b-cycles
rm -rf $T/np4-work
{ python3 -B $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/newplants.py $L $L/third_party/lwSRP $T/np4-work step-beside-input,plat-store-tick-unbound,plat-store-step-unbound; echo "rc=$?"; } > $T/logs/newplants4.log 2>&1

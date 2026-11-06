#!/bin/bash
# The new plants on a checkout (a pre-check, not a gate). usage: newplants.sh CHECKOUT TAG [NAMES]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
C=$1 TAG=$2
export TMPDIR=$T/tmp/np-$TAG; mkdir -p $TMPDIR
rm -rf $T/np-$TAG-work
cd "$C" && { python3 -B $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/newplants.py $C $T/np-$TAG-work ${3:-}; echo "rc=$?"; } > $T/logs/newplants-$TAG.log 2>&1

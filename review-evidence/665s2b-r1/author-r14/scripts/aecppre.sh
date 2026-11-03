#!/bin/bash
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683q
export TMPDIR=$T/tmp/aecp-$2; mkdir -p $TMPDIR; rm -rf $T/aecp-$2-work
cd "$1" && { python3 -B $MANAGEMENT/2026-09-23/665s2b-a683q/scripts/aecpplants.py "$1" $T/aecp-$2-work "$3"; echo "rc=$?"; } > $T/logs/aecppre-$2.log 2>&1

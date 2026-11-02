#!/bin/bash
# Start legs one after another, each once the one before has its native model or has ended, so that no two run the
# CPU generator at once (sbt holds one build at a time); then wait for all.
# usage: chain.sh "CHECKOUT NAME POINT GROUPS [args...]" ...
set -u
B=$VALIDATION_STORAGE/665s2b-a683o/builds
L=$VALIDATION_STORAGE/665s2b-a683o/logs
for leg in "$@"; do
    set -- $leg
    name=$2
    $MANAGEMENT/2026-09-23/665s2b-a683o/scripts/leg.sh $leg &
    until [ -x "$B/$name/native/Vsim" ] || grep -q '^rc=' "$L/$name.log" 2>/dev/null; do
        read -t 10 < /dev/zero || true
        python3 -c 'import time; time.sleep(10)'
    done
done
wait

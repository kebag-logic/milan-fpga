#!/bin/bash
# The legs' images rebuilt at a head through the harness's own build.firmware(), one log and rc.
# usage: imgcheck.sh [CHECKOUT OUT LOG]; defaults are the first final-head run's.
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
C=${1:-$T/IMG} O=${2:-$T/img-final} LOG=${3:-$T/logs/imgcheck.log}
cd "$C" || exit 3
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/imgcheck.py "$C" "$O" $T/builds N-A1:endstation_ax7101_1x1_tdm8:1:none:none N-B1:endstation_ax7101_1x1_tdm8:1:none:answering-ports N-A8:endstation_ax7101_8x8:2:none:none N-B8:endstation_ax7101_8x8:2:none:answering-ports; echo "rc=$?"; } > "$LOG" 2>&1

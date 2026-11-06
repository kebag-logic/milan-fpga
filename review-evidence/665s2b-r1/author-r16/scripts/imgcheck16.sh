#!/bin/bash
# The measured legs' images rebuilt at the final head through the harness's own build.firmware(), one log and rc.
# usage: imgcheck16.sh CHECKOUT OUT LOG
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
C=$1 O=$2 LOG=$3
cd "$C" || exit 3
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/imgcheck.py "$C" "$O" $T/builds N-A1:endstation_ax7101_1x1_tdm8:1:none:none N-B1:endstation_ax7101_1x1_tdm8:1:none:answering-ports N-A8:endstation_ax7101_8x8:2:none:none N-B8:endstation_ax7101_8x8:2:none:answering-ports NT-1:endstation_ax7101_1x1_tdm8:1:none:answering-later NT-8:endstation_ax7101_8x8:2:none:answering-later TB-8:endstation_ax7101_8x8:2:transmit-beside-records:answering-later RA-8:endstation_ax7101_8x8:2:retry-ageless:answering-later AH-A8:endstation_ax7101_8x8:2:store-step-aged-heavier:none; echo "rc=$?"; } > "$LOG" 2>&1

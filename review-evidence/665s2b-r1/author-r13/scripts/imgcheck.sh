#!/bin/bash
# The legs' images rebuilt at the final head, one log and rc.
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
cd $VALIDATION_STORAGE/665s2b-a683p/IMG3
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/imgcheck.py $VALIDATION_STORAGE/665s2b-a683p/IMG3 $VALIDATION_STORAGE/665s2b-a683p/img-final3 $VALIDATION_STORAGE/665s2b-a683p/builds N-A1:endstation_ax7101_1x1_tdm8:1:none:none N-B1:endstation_ax7101_1x1_tdm8:1:none:answering-ports N-A8:endstation_ax7101_8x8:2:none:none N-B8:endstation_ax7101_8x8:2:none:answering-ports CTL-A8:endstation_ax7101_8x8:2:store-step-unbounded:none; echo "rc=$?"; } > $VALIDATION_STORAGE/665s2b-a683p/logs/imgcheck.log 2>&1

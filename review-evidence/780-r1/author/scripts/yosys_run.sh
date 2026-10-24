#!/usr/bin/env bash
# #780: the full serial Yosys gate (Yosys 0.66, sv2v v0.0.12) in a clean clone at the head.
X=$VALIDATION_STORAGE/scratch/780-a670; D=$(cd "$(dirname "$0")" && pwd)
cd $X/clone-yosys || exit 2
source $D/env.sh
yosys -V > $X/r/yosys/versions.txt; sv2v --version >> $X/r/yosys/versions.txt
s=$(date +%s); bash syn/yosys/run.sh --results $X/yosys-results > $X/r/yosys/run.log 2>&1; echo $? > $X/r/yosys/run.rc
echo "$(( $(date +%s)-s ))s" > $X/r/yosys/seconds.txt
git status --porcelain --untracked-files=no > $X/r/yosys/clone-status-after.txt

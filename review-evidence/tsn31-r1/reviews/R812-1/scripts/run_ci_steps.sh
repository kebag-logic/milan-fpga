#!/bin/bash
# Run the quality.yml testing run: steps on a clean clone. usage: run_ci_steps.sh <packet> <clone> <tag> <validate-jobs> <rv32-jobs>
P=$1 C=$2 TAG=$3 VJ=$4 RJ=$5
. "$P/scripts/env.sh" "$P"
R=$P/receipts; cd "$C" || exit 9
git rev-parse HEAD > "$R/$TAG.head"; git status --porcelain > "$R/$TAG.status-before"
{ which clang clang++ clang-18 gcc g++ clang-tidy mmdc cmake; clang --version | head -1; gcc --version | head -1; clang-tidy --version | sed -n 2p; pkg-config --modversion gtest gmock; } > "$R/$TAG.tools" 2>&1
( /usr/bin/time -v python3 scripts/baremetal.py --work build-rv32 --jobs $RJ > "$R/$TAG.rv32.log" 2> "$R/$TAG.rv32.time"; echo $? > "$R/$TAG.rv32.rc" ) &
( /usr/bin/time -v python3 scripts/validate.py --work build-validation --jobs $VJ --graphs > "$R/$TAG.validate.log" 2> "$R/$TAG.validate.time"; echo $? > "$R/$TAG.validate.rc" ) &
wait
git status --porcelain > "$R/$TAG.status-after"; git diff --stat > "$R/$TAG.diff-after"
echo done > "$R/$TAG.done"

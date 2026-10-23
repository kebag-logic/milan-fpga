#!/usr/bin/env bash
# The builder bank at the lane head, as rounds 2 and 3 ran it; logs under $1.
set -u
L=$1; mkdir -p "$L"
cd $VALIDATION_STORAGE/scratch/632-a659/r6/clone-light-0ffcd7f0
export MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
git rev-parse HEAD > "$L/builder.head"
date -Is > "$L/builder.start"
$WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > "$L/builder.log" 2>&1
echo $? > "$L/builder.rc"
date -Is > "$L/builder.end"

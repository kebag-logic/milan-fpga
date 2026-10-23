#!/usr/bin/env bash
# The builder bank at the lane head, as round 2 ran it.
set -u
L=$VALIDATION_STORAGE/scratch/632-a659/r3/logs
cd $LANES/632-phase
export MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
git rev-parse HEAD > $L/builder.head
date -Is > $L/builder.start
$WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > $L/builder.log 2>&1
echo $? > $L/builder.rc
date -Is > $L/builder.end

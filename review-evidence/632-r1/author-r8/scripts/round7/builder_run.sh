#!/usr/bin/env bash
# The builder bank at the lane head, as rounds 2 to 6 ran it (the LiteX
# interpreter, --require-elaboration --require-rv32), in a clean clone.
# usage: builder_run.sh <clone> <log dir>
set -u
C=$1; L=$2; mkdir -p "$L"
cd "$C" || exit 2
export MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$PATH
git rev-parse HEAD > "$L/builder.head"
date -Is > "$L/builder.start"
$WORKSPACE_HOME/litex-milan/venv/bin/python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > "$L/builder.log" 2>&1
echo $? > "$L/builder.rc"
date -Is > "$L/builder.end"

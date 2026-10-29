#!/bin/bash
# The docs, scope, idiom, harness, CPU option and behave gates at a clone's head, one at a time (gates_s3.py),
# without the end-station builder gate, which runs in its own clone. Scratch goes to the lane's disk scratch.
# usage: docs_gates.sh CLONE OUT
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697d/scripts
export GATE_HDL_PYTHON=$VALIDATION_STORAGE/665s3-a697c/venv-hdl/bin/python3
export GATE_BUILDER_PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin
export PATH=$WORKSPACE_HOME/.local/bin:$PATH
P=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3
X=$VALIDATION_STORAGE/665s3-a697d/docs-scratch-$(git -C "$1" rev-parse --short=8 HEAD)
mkdir -p "$2" "$X"
$P -B $S/gates_s3.py "$1" $P "$2" "$X" -builder_require_rv32 > "$2/runner.out" 2>&1
rc=$?
echo "rc=$rc" >> "$2/runner.out"
exit $rc

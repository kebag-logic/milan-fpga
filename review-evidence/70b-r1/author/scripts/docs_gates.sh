#!/bin/bash
# The docs, scope, idiom, harness self-tests, host firmware checks, CPU option and behave gates at a
# clone's head, one at a time (gates_a704.py). Scratch goes to the lane's disk.
# usage: docs_gates.sh CLONE OUT [NAME...]
set -u
S=$MANAGEMENT/2026-09-23/70-a704/scripts
export GATE_HDL_PYTHON=$VALIDATION_STORAGE/665s2b-a683l/venv-hdl/bin/python3
export GATE_BUILDER_PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin
export PATH=$WORKSPACE_HOME/.local/bin:$PATH
P=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3
C=$1 O=$2; shift 2
X=$VALIDATION_STORAGE/scratch/70-a704/docs-scratch-$(git -C "$C" rev-parse --short=8 HEAD)
mkdir -p "$O" "$X"
$P -B $S/gates_a704.py "$C" $P "$O" "$X" "$@" > "$O/runner.out" 2>&1
rc=$?
echo "rc=$rc" >> "$O/runner.out"
exit $rc

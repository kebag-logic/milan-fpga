#!/bin/bash
# The docs workflow, bare-metal scope, idiom, harness, CPU option and behave gates at the head in their own clone, one
# at a time (gates_s2b3.py), without the end-station builder gate, which runs in its own clone.
# usage: docs_gates.sh CHECKOUT OUT_DIR
set -u
T=$VALIDATION_STORAGE/665s2b-a683m
export GATE_HDL_PYTHON=$VALIDATION_STORAGE/665s2b-a683l/venv-hdl/bin/python3
export GATE_BUILDER_PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin
export PATH=$WORKSPACE_HOME/.local/bin:$PATH
P=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3
C=$1 O=$2
mkdir -p "$O" $T/docs-scratch
$P -B $MANAGEMENT/2026-09-23/665s2b-a683m/scripts/gates_s2b3.py "$C" $P "$O" $T/docs-scratch \
  -builder_require_rv32 > "$O/runner.out" 2>&1
echo "rc=$?" >> "$O/runner.out"

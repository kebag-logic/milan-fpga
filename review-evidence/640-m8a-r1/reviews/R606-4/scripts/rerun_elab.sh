#!/bin/bash
# The elaboration gate alone, after run 1 overlapped the docs-job builder gate in the same clone.
set -u
. "$PACKET/scripts/env.sh"
export PATH=$S/litex-venv/bin:$PATH
R=$PACKET/receipts/litex
cd "$CLONE" || exit 9
python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > "$R/test_builder_elab.log" 2>&1
echo $? > "$R/test_builder_elab.rc"

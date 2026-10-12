#!/bin/bash
# LiteX campaign at the reviewed head, as elaborate.yml runs it, in a pins-only interpreter.
# usage: campaign_litex.sh  (PACKET and CLONE exported)
set -u
. "$PACKET/scripts/env.sh"
export PATH=$S/litex-venv/bin:$PATH
R=$PACKET/receipts/litex
mkdir -p "$R"
cd "$CLONE" || exit 9
step() { name=$1; shift; "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
step ci_scope_selftest python3 scripts/ci_scope.py --selftest
step sims_selftest scripts/run_litex_sims.sh --selftest
step sims_aggregate scripts/run_litex_sims.sh "$S/litex-sim-logs"
step test_builder_elab python3 sw/builder/test_builder.py --require-elaboration --require-rv32
echo done > "$R/DONE"

#!/bin/bash
# Contract and generator checks at the working tree; one log and rc per command.
cd $LANES/748-elab-race || exit 2
P=$VALIDATION_STORAGE/748-a623/gatevenv/bin/python3
O=$VALIDATION_STORAGE/748-a623/r2/gates
run() { local tag=$1; shift; "$@" > "$O/$tag.log" 2>&1; echo $? > "$O/$tag.rc"; }
run gw_check $P scripts/ci_gate_workflows.py --check
run gw_selftest $P scripts/ci_gate_workflows_selftest.py
run ev_check $P scripts/ci_events.py --check
run ev_selftest $P scripts/ci_events.py --selftest
echo done > "$O/done"

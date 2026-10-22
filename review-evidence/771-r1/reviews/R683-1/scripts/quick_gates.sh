#!/usr/bin/env bash
# Usage: quick_gates.sh REPO OUTDIR  - runs the record/consistency gates concurrently, one log + rc each.
set -u
R=$1; O=$2; mkdir -p "$O"; cd "$R" || exit 2
export PYTHONHASHSEED=0 VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
run() { n=$1; shift; ( "$@" >"$O/$n.log" 2>&1; echo $? >"$O/$n.rc" ) & }
run resource_check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run diag_submodule python3 docs/diagrams/submodule_boundaries.gen.py --check
run diag_timesync python3 docs/diagrams/timesync_chain.gen.py --check
run submodule_docs python3 scripts/check_submodule_docs.py
run gptp_docs python3 scripts/check_gptp_docs.py --with-submodule
run port_contracts python3 scripts/check_port_contracts.py
run naming python3 scripts/measure_naming.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run lint_rtl python3 scripts/lint_rtl.py --check
run nvm_capture python3 scripts/check_nvm_capture.py
run integrator_params python3 protocol-processor/scripts/check-integrator-params.py
wait
for f in "$O"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

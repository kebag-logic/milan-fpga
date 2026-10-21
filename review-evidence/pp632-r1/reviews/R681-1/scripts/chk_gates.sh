#!/usr/bin/env bash
# Docs gates, HDL lint, the uPC/M9 guards and the focused AECP suites, in one
# clean clone at the reviewed head. Each step prints its own rc; the script's rc
# is the number of failing steps.
set -u
V=${V:?set V to the pinned Verilator 5.050 executable}
export PATH=$(dirname "$V"):$PATH
fails=0
step() { echo "=== STEP $*"; "$@"; rc=$?; echo "=== RC $rc : $*"; [ $rc = 0 ] || fails=$((fails+1)); }
git rev-parse HEAD HEAD^{tree}
step make check
step ./scripts/lint_hdl.sh
step python3 scripts/check_upc_map.py
step python3 scripts/check_m9_opcodes.py --selftest
step python3 scripts/check_m9_opcodes.py
for s in aecp_cmds ucpu dyn_state aecp_notify; do step make -C tb/$s VERILATOR="$V"; done
step python3 -B tb/aecp_cmds/mutants.py --output "${OUT:-/tmp}/aecp-cmds-mutants" --verilator "$V"
step python3 scripts/gen_matrix.py --check
echo "gates: $fails failing"
exit $fails

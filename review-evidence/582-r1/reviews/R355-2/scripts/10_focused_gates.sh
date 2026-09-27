#!/bin/bash
# Run the focused #582 gates on a tree.
# Usage: 10_focused_gates.sh <tree> [python-with-migen]
# The capture receipt gate needs real submodule git metadata, so run it on the clone.
set -u
T=${1:?tree}; PY=${2:-python3}; cd "$T" || exit 2
run() { local name=$1; shift; echo "=== $name: $*"; "$@"; echo "=== $name rc=$?"; }
run clock-contract "$PY" sw/builder/test_clock_contract.py --soc
run declarations "$PY" sw/builder/test_declarations.py
run capture "$PY" scripts/check_nvm_capture.py
(cd sw/litex && run pp-mem-bridge "$PY" test_pp_mem_bridge.py)

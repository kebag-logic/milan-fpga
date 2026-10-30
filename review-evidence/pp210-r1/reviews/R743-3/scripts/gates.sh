#!/usr/bin/env bash
# Run every repository gate of the docs-gates job plus the gate preamble of the
# suites job in one checkout; one log and one rc line per gate.
# usage: gates.sh <checkout> <outdir> ; needs VERILATOR_DIR on PATH for lint_hdl.sh
set -u
# put a python3 that imports the pinned wavedrom first: export PATH=<venv>/bin:$PATH
tree=$1; out=$2; mkdir -p "$out"; cd "$tree" || exit 2
run() { local name=$1; shift; "$@" >"$out/$name.log" 2>&1; echo "$name rc=$?" | tee -a "$out/rc.txt"; }
: >"$out/rc.txt"
echo "head $(git rev-parse HEAD)" >"$out/rc.txt"
run make_check make check
run gen_matrix_check python3 scripts/gen_matrix.py --check
run check_upc_map python3 scripts/check_upc_map.py
run check_m9_selftest python3 scripts/check_m9_opcodes.py --selftest
run check_m9 python3 scripts/check_m9_opcodes.py
run lint_hdl ./scripts/lint_hdl.sh
git status --porcelain >"$out/status-after.txt"

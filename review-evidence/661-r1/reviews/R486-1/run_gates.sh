#!/bin/bash
# Run the light consumer gates at the checked-out tree in parallel; one log and rc per gate.
# Usage: run_gates.sh <repo> <outdir>. Requires the pinned Verilator and the pinned Markdown venv on PATH.
repo=$1; out=$2; mkdir -p "$out"; cd "$repo" || exit 2
cat > "$out/gates.list" <<'LIST'
cpp_idiom|python3 scripts/check_cpp_idiom.py
py_idiom|python3 scripts/check_py_idiom.py
sh_idiom|python3 scripts/check_sh_idiom.py
rtl_source_lists|python3 scripts/check_rtl_source_lists.py
rtl_source_lists_selftest|python3 scripts/check_rtl_source_lists.py --selftest
pp_srcs|python3 scripts/pp_srcs.py --check --selftest
port_contracts|python3 scripts/check_port_contracts.py
naming|python3 scripts/measure_naming.py --check
test_evidence|python3 scripts/measure_test_evidence.py --check
docs_check|python3 scripts/docs_check.py
lint_rtl|python3 scripts/lint_rtl.py --check --self-test
nvm_capture|python3 scripts/check_nvm_capture.py
submodule_docs|python3 scripts/check_submodule_docs.py
boundary_diagram|python3 docs/diagrams/submodule_boundaries.gen.py --check
em_dash|python3 scripts/check_em_dash.py --base 506d91dbeeba585d72d2e80d92fca799c719f8ee
em_dash_selftest|python3 scripts/check_em_dash.py --selftest
resource_gate_baseline|python3 syn/ooc/pp_resource_gate.py check-baseline
LIST
run_one() { name=${1%%|*}; cmd=${1#*|}; bash -c "$cmd" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc"; }
export -f run_one; export out
xargs -d '\n' -P 8 -I{} bash -c 'run_one "$@"' _ {} < "$out/gates.list"
for f in "$out"/*.rc; do printf '%s rc %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

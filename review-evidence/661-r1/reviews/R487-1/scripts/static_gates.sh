#!/usr/bin/env bash
# Run the parent's static/record gates for this adoption in a checkout, concurrently, one log and rc each.
# Usage: static_gates.sh <checkout> <receipt-dir> <tag>
set -u
root=$1; out=$2; tag=$3; mkdir -p "$out"
cd "$root"
run() { local id=$1; shift; ( timeout 1500 "$@" > "$out/${tag}_$id.log" 2>&1; echo $? > "$out/${tag}_$id.rc" ) & }
run rtl_source_lists python3 scripts/check_rtl_source_lists.py
run rtl_source_lists_selftest python3 scripts/check_rtl_source_lists.py --selftest
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run port_contracts python3 scripts/check_port_contracts.py
run measure_naming python3 scripts/measure_naming.py --check
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run docs_check python3 scripts/docs_check.py
run nvm_capture python3 scripts/check_nvm_capture.py
run submodule_docs python3 scripts/check_submodule_docs.py
run boundary_diagram python3 docs/diagrams/submodule_boundaries.gen.py --check
run py_idiom python3 scripts/check_py_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run sh_idiom python3 scripts/check_sh_idiom.py
run lint_rtl python3 scripts/lint_rtl.py --check --self-test
wait
for f in "$out/${tag}"_*.rc; do printf '%-60s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
